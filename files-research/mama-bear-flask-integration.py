"""
🐻 Mama Bear Flask API Integration
Combines Scrapybara desktop control with intelligent Gemini quota management
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import asyncio
from datetime import datetime
import json
from typing import Dict, Any, Optional
import logging
from scrapybara import Scrapybara
from scrapybara.tools import ComputerTool, BashTool, EditTool

# Import our quota manager
from mama_bear_quota_manager import (
    MamaBearQuotaManager, 
    MamaBearAgent,
    ModelType,
    MAMA_BEAR_CONFIG
)

app = Flask(__name__)
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MamaBearAPI")

# Global instances
mama_bear_agent = None
scrapybara_client = None
active_sessions = {}  # Track active Scrapybara sessions

def initialize_mama_bear():
    """Initialize Mama Bear with enhanced configuration"""
    global mama_bear_agent, scrapybara_client
    
    # Enhanced config with your specific models
    config = {
        "billing_accounts": [
            {
                "id": "primary_account",
                "api_key": os.environ.get("GEMINI_API_KEY_1"),
                "is_primary": True
            },
            {
                "id": "secondary_account", 
                "api_key": os.environ.get("GEMINI_API_KEY_2"),
                "is_primary": False
            }
        ],
        "models": {
            "pro": "gemini-2.5-pro-preview-05-06",
            "flash_stable": "gemini-2.5-flash-preview-04-17",
            "flash_latest": "gemini-2.5-flash-preview-05-20"
        }
    }
    
    mama_bear_agent = MamaBearAgent(config)
    
    # Initialize Scrapybara
    try:
        scrapybara_client = Scrapybara()
        logger.info("✅ Scrapybara initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️ Scrapybara initialization failed: {e}")

@app.route('/api/mama-bear/think', methods=['POST'])
async def mama_bear_think():
    """
    🐻 Main endpoint for Mama Bear interactions
    Automatically handles quota limits and model selection
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        task_type = data.get('task_type', 'general')
        context = data.get('context', {})
        
        # Let Mama Bear think with automatic failover
        response = await mama_bear_agent.think(
            prompt=prompt,
            context=context,
            task_type=task_type
        )
        
        return jsonify({
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in mama_bear_think: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/mama-bear/create-workspace', methods=['POST'])
async def create_workspace():
    """
    🐻 Create a new development workspace with Scrapybara
    Uses intelligent model selection for setup instructions
    """
    try:
        data = request.json
        project_description = data.get('project_description')
        requirements = data.get('requirements', [])
        
        # Start Scrapybara instance
        instance = scrapybara_client.start_ubuntu()
        
        # Prepare tools
        tools = [
            ComputerTool(instance),
            BashTool(instance),
            EditTool(instance)
        ]
        
        # Get setup instructions from Mama Bear (with quota management)
        setup_prompt = f"""
        🐻 Create the perfect development environment for:
        Project: {project_description}
        Requirements: {', '.join(requirements)}
        
        Steps:
        1. Install all necessary tools and dependencies
        2. Set up the project structure
        3. Configure the IDE (VS Code)
        4. Create initial boilerplate code
        5. Set up version control
        
        Make it exactly how a developer would love it!
        """
        
        # Get response with automatic model failover
        result = await mama_bear_agent.quota_manager.get_response(
            prompt=setup_prompt,
            task_type="code_generation",
            complexity="high"
        )
        
        if result["success"]:
            # Execute setup with Scrapybara
            response = scrapybara_client.act(
                tools=tools,
                model=result["model_used"],  # Use the same model that worked
                prompt=result["response"]
            )
            
            # Store session info
            session_id = f"workspace_{datetime.now().timestamp()}"
            active_sessions[session_id] = {
                "instance_id": instance.id,
                "project": project_description,
                "created_at": datetime.now().isoformat(),
                "model_used": result["model_used"],
                "account_used": result["account_used"]
            }
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "instance_url": instance.url,
                "setup_details": response,
                "model_used": result["model_used"]
            })
        else:
            return jsonify({
                "success": False,
                "error": "All models are currently unavailable",
                "health_status": mama_bear_agent.quota_manager.get_health_status()
            }), 503
            
    except Exception as e:
        logger.error(f"Error creating workspace: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/mama-bear/health', methods=['GET'])
def get_health_status():
    """
    🐻 Get current health status of all models and accounts
    """
    health = mama_bear_agent.quota_manager.get_health_status()
    
    # Add Scrapybara status
    health["scrapybara"] = {
        "available": scrapybara_client is not None,
        "active_sessions": len(active_sessions)
    }
    
    return jsonify(health)

@app.route('/api/mama-bear/stream', methods=['POST'])
async def stream_response():
    """
    🐻 Stream responses with automatic failover
    Perfect for long-running tasks
    """
    data = request.json
    prompt = data.get('prompt')
    task_type = data.get('task_type', 'general')
    
    async def generate():
        # Try each model in order until one works
        models = ModelSelector.select_model_for_task(task_type)
        
        for model_type in models:
            for account in mama_bear_agent.quota_manager.accounts:
                try:
                    # Configure client
                    mama_bear_agent.quota_manager._get_client(account)
                    
                    # Create model
                    model = genai.GenerativeModel(
                        model_name=model_type.value,
                        system_instruction=mama_bear_agent._build_system_prompt({})
                    )
                    
                    # Stream response
                    async for chunk in model.generate_content_async(
                        prompt,
                        stream=True
                    ):
                        if chunk.text:
                            yield f"data: {json.dumps({'text': chunk.text, 'model': model_type.value})}\n\n"
                    
                    yield f"data: {json.dumps({'done': True, 'model': model_type.value})}\n\n"
                    return
                    
                except Exception as e:
                    logger.warning(f"Model {model_type.value} failed: {e}")
                    continue
        
        # All models failed
        yield f"data: {json.dumps({'error': 'All models unavailable'})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/api/mama-bear/smart-retry', methods=['POST'])
async def smart_retry():
    """
    🐻 Intelligent retry with different models
    Useful for complex tasks that might fail with one model
    """
    data = request.json
    prompt = data.get('prompt')
    previous_model = data.get('previous_model')
    previous_error = data.get('previous_error')
    
    # Build enhanced prompt with error context
    enhanced_prompt = f"""
    Previous attempt with {previous_model} failed with: {previous_error}
    
    Please try a different approach:
    {prompt}
    """
    
    # Get models excluding the failed one
    all_models = list(ModelType)
    if previous_model:
        all_models = [m for m in all_models if m.value != previous_model]
    
    # Try with remaining models
    for model_type in all_models:
        result = await mama_bear_agent.quota_manager.get_response(
            prompt=enhanced_prompt,
            task_type="recovery",
            max_retries=1
        )
        
        if result["success"]:
            return jsonify(result)
    
    return jsonify({
        "success": False,
        "error": "All retry attempts failed",
        "health_status": mama_bear_agent.quota_manager.get_health_status()
    }), 503

# WebSocket support for real-time updates
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('mama_bear_chat')
async def handle_chat(data):
    """
    🐻 Real-time chat with Mama Bear
    Automatically switches models on quota errors
    """
    prompt = data.get('prompt')
    session_id = data.get('session_id')
    
    # Emit thinking status
    emit('thinking', {'status': 'Mama Bear is thinking...'})
    
    # Get response with failover
    result = await mama_bear_agent.quota_manager.get_response(
        prompt=prompt,
        task_type="chat"
    )
    
    if result["success"]:
        emit('response', {
            'text': result["response"],
            'model_used': result["model_used"],
            'attempts': result["attempts"]
        })
    else:
        emit('error', {
            'message': 'All models are currently busy',
            'retry_in': 60
        })

# Background task to monitor and heal quota issues
async def quota_monitor():
    """
    🐻 Background task to monitor and reset cooldowns
    """
    while True:
        health = mama_bear_agent.quota_manager.get_health_status()
        
        if health["overall_health"] == "critical":
            logger.warning("🚨 Critical: All models in cooldown")
            
            # Check if any cooldowns can be reset
            for account in mama_bear_agent.quota_manager.accounts:
                for model_type, stats in account.stats.items():
                    if stats.cooldown_until and datetime.now() > stats.cooldown_until:
                        stats.cooldown_until = None
                        stats.quota_errors = 0  # Reset error count
                        logger.info(f"✅ Reset cooldown for {model_type.value}")
        
        await asyncio.sleep(60)  # Check every minute

# Error handlers
@app.errorhandler(500)
def handle_error(e):
    logger.error(f"Internal error: {e}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "mama_bear_says": "🐻 Don't worry, I'm looking into this!"
    }), 500

# Initialize on startup
@app.before_first_request
def startup():
    initialize_mama_bear()
    
    # Start background monitor
    asyncio.create_task(quota_monitor())

if __name__ == '__main__':
    # Run with async support
    socketio.run(app, debug=True, port=5000)
