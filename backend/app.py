# backend/app.py
"""
🐻 Podplay Sanctuary - Advanced Mama Bear Backend
Complete AI-powered development sanctuary with intelligent orchestration
"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Import all Mama Bear systems
from services.mama_bear_complete_system import initialize_complete_system, get_mama_bear_system
from services.mama_bear_model_manager import MamaBearModelManager
from services.mama_bear_orchestration import initialize_orchestration
from services.mama_bear_memory_system import initialize_enhanced_memory
from services.mama_bear_workflow_logic import initialize_workflow_intelligence
from services.mama_bear_monitoring import MamaBearMonitoring

# Import enhanced features
from services.enhanced_scrapybara_manager import enhanced_scrapybara
from services.enhanced_mama_bear_orchestrator import mama_bear_orchestrator, TaskType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('podplay_sanctuary.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'mama-bear-sanctuary-2024')

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Enable CORS
CORS(app)

# Global system reference
mama_bear_system = None

@app.route('/')
def index():
    """Main landing page"""
    return jsonify({
        'service': 'Podplay Sanctuary Backend',
        'status': 'active',
        'mama_bear': '🐻 Ready to help!',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'Advanced Model Management',
            'Intelligent Agent Orchestration', 
            'Enhanced Memory System',
            'Real-time Monitoring',
            'Workflow Intelligence',
            'Multi-Agent Collaboration'
        ]
    })

@app.route('/api/health')
async def health_check():
    """Comprehensive health check"""
    try:
        system = get_mama_bear_system()
        if system and system.is_initialized:
            health_status = await system.get_system_status()
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'system_status': health_status
            })
        else:
            return jsonify({
                'status': 'initializing',
                'timestamp': datetime.now().isoformat(),
                'message': 'Mama Bear is waking up...'
            }), 202
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/api/status')
async def get_status():
    """Get detailed system status"""
    try:
        system = get_mama_bear_system()
        if not system:
            return jsonify({'status': 'not_initialized'}), 503
        
        status = await system.get_system_status()
        return jsonify(status)
    
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/monitoring/dashboard')
async def monitoring_dashboard():
    """Get monitoring dashboard data"""
    try:
        system = get_mama_bear_system()
        if not system or not system.monitoring:
            return jsonify({'error': 'Monitoring not available'}), 503
        
        dashboard_data = await system.monitoring.get_monitoring_dashboard()
        return jsonify(dashboard_data)
    
    except Exception as e:
        logger.error(f"Dashboard request failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/status')
async def models_status():
    """Get model manager status"""
    try:
        system = get_mama_bear_system()
        if not system or not system.model_manager:
            return jsonify({'error': 'Model manager not available'}), 503
        
        model_status = await system.model_manager.get_status()
        return jsonify(model_status)
    
    except Exception as e:
        logger.error(f"Model status request failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/status')
async def agents_status():
    """Get agent status"""
    try:
        system = get_mama_bear_system()
        if not system or not system.orchestrator:
            return jsonify({'error': 'Orchestrator not available'}), 503
        
        orchestrator_status = await system.orchestrator.get_orchestration_status()
        
        # Get individual agent status
        agent_details = {}
        for name, agent in system.agents.items():
            agent_details[name] = {
                'name': agent.name,
                'initialized': hasattr(agent, 'is_initialized') and agent.is_initialized,
                'capabilities': agent.capabilities,
                'active_sessions': getattr(agent, 'active_sessions', 0),
                'last_activity': getattr(agent, 'last_activity', None)
            }
        
        return jsonify({
            'orchestrator_status': orchestrator_status,
            'agents': agent_details
        })
    
    except Exception as e:
        logger.error(f"Agent status request failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/memory/stats')
async def memory_stats():
    """Get memory system statistics"""
    try:
        system = get_mama_bear_system()
        if not system or not system.memory_manager:
            return jsonify({'error': 'Memory manager not available'}), 503
        
        memory_status = await system.memory_manager.get_status()
        return jsonify(memory_status)
    
    except Exception as e:
        logger.error(f"Memory stats request failed: {e}")
        return jsonify({'error': str(e)}), 500

# Chat endpoints
@app.route('/api/chat', methods=['POST'])
async def chat():
    """Main chat endpoint for all agents"""
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        page_context = data.get('page_context', 'main_chat')
        attachments = data.get('attachments', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        system = get_mama_bear_system()
        if not system:
            return jsonify({'error': 'System not initialized'}), 503
        
        # Get appropriate agent for context
        agent = system._get_agent_for_context(page_context)
        
        # Process message
        response = await agent.process_message(
            message=message,
            user_id=user_id,
            context={
                'page': page_context,
                'attachments': attachments,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Log interaction for monitoring
        if system.monitoring:
            await system.monitoring.log_interaction(
                user_id=user_id,
                agent=agent.name,
                message=message,
                response=response
            )
        
        return jsonify({
            'success': True,
            'response': response['content'] if response.get('success') else response.get('error'),
            'agent': agent.name,
            'model_used': response.get('model_used'),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Chat request failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Agent Plan endpoints
@app.route('/api/plans', methods=['POST'])
async def create_plan():
    """Create an agent execution plan"""
    try:
        data = request.json
        title = data.get('title', '')
        description = data.get('description', '')
        user_id = data.get('user_id', 'anonymous')
        context = data.get('context', {})
        
        if not title or not description:
            return jsonify({'error': 'Title and description are required'}), 400
        
        system = get_mama_bear_system()
        if not system or not system.orchestrator:
            return jsonify({'error': 'Orchestrator not available'}), 503
        
        # Create plan through orchestrator
        plan = await system.orchestrator.create_plan(
            title=title,
            description=description,
            user_id=user_id,
            context=context
        )
        
        return jsonify({
            'success': True,
            'plan': plan,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Plan creation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/plans/<plan_id>')
async def get_plan(plan_id):
    """Get plan details"""
    try:
        system = get_mama_bear_system()
        if not system or not system.orchestrator:
            return jsonify({'error': 'Orchestrator not available'}), 503
        
        plan = system.orchestrator.get_plan(plan_id)
        return jsonify({
            'success': True,
            'plan': plan,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Plan retrieval failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 404

@app.route('/api/plans/<plan_id>/subtasks/<subtask_id>/run', methods=['POST'])
async def run_subtask(plan_id, subtask_id):
    """Execute a subtask"""
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        
        system = get_mama_bear_system()
        if not system or not system.orchestrator:
            return jsonify({'error': 'Orchestrator not available'}), 503
        
        result = await system.orchestrator.run_subtask(plan_id, subtask_id, user_id)
        
        return jsonify({
            'success': result['success'],
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Subtask execution failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# VM Management endpoints
@app.route('/api/vm/create', methods=['POST'])
async def create_vm():
    """Create a VM instance"""
    try:
        data = request.json
        config = data.get('config', {})
        user_id = data.get('user_id', 'anonymous')
        
        system = get_mama_bear_system()
        if not system:
            return jsonify({'error': 'System not available'}), 503
        
        instance = await system.create_vm_instance(config, user_id)
        
        return jsonify({
            'success': instance['success'],
            'instance': instance,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"VM creation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Scout autonomous task endpoint
@app.route('/api/scout/execute', methods=['POST'])
async def execute_scout_task():
    """Execute an autonomous Scout task"""
    try:
        data = request.json
        task_description = data.get('task_description', '')
        user_id = data.get('user_id', 'anonymous')
        context = data.get('context', {})
        
        if not task_description:
            return jsonify({'error': 'Task description is required'}), 400
        
        system = get_mama_bear_system()
        if not system:
            return jsonify({'error': 'System not available'}), 503
        
        result = await system.process_autonomous_task(task_description, user_id, context)
        
        return jsonify({
            'success': result['success'],
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Scout task execution failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_status', {
        'status': 'connected',
        'message': '🐻 Mama Bear is ready to help!',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('mama_bear_message')
async def handle_mama_bear_message(data):
    """Handle real-time Mama Bear messages"""
    try:
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        attachments = data.get('attachments', [])
        
        if not message:
            emit('mama_bear_error', {'error': 'Message is required'})
            return
        
        system = get_mama_bear_system()
        if not system:
            emit('mama_bear_error', {'error': 'System not available'})
            return
        
        # Get appropriate agent
        agent = system._get_agent_for_context(page_context)
        
        # Process message
        response = await agent.process_message(
            message=message,
            user_id=user_id,
            context={
                'page': page_context,
                'attachments': attachments,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Send response
        emit('mama_bear_response', {
            'response': response['content'] if response.get('success') else response.get('error'),
            'agent': agent.name,
            'model_used': response.get('model_used'),
            'page_context': page_context,
            'timestamp': datetime.now().isoformat(),
            'success': response.get('success', False)
        })
        
        # Log for monitoring
        if system.monitoring:
            await system.monitoring.log_interaction(
                user_id=user_id,
                agent=agent.name,
                message=message,
                response=response
            )
    
    except Exception as e:
        logger.error(f"SocketIO message handling failed: {e}")
        emit('mama_bear_error', {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

@socketio.on('get_system_status')
async def handle_system_status():
    """Handle system status requests"""
    try:
        system = get_mama_bear_system()
        if system:
            status = await system.get_system_status()
            emit('system_status', status)
        else:
            emit('system_status', {'status': 'not_initialized'})
    except Exception as e:
        logger.error(f"System status request failed: {e}")
        emit('system_status', {'error': str(e)})

# 🚀 Enhanced Computer Use Agent & Browser Routes
@app.route('/api/enhanced/submit-task', methods=['POST'])
async def submit_enhanced_task():
    """Submit a task to the enhanced orchestrator"""
    try:
        data = request.json
        task_description = data.get('description')
        task_type_str = data.get('task_type', 'research')
        user_id = data.get('user_id', 'anonymous')
        priority = data.get('priority', 1)
        
        # Convert string to TaskType enum
        task_type = TaskType(task_type_str)
        
        task_id = await mama_bear_orchestrator.submit_task(
            task_description=task_description,
            task_type=task_type,
            user_id=user_id,
            priority=priority
        )
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': f'Task submitted successfully: {task_id}'
        })
        
    except Exception as e:
        logger.error(f"Enhanced task submission error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/enhanced/shared-browser/create', methods=['POST'])
async def create_shared_browser():
    """Create a shared browser session"""
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        initial_url = data.get('initial_url')
        
        session = await enhanced_scrapybara.create_shared_browser_session(
            user_id=user_id,
            initial_url=initial_url
        )
        
        return jsonify({
            'success': True,
            'session': {
                'session_id': session.session_id,
                'instance_id': session.instance_id,
                'url': session.url,
                'created_at': session.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Shared browser creation error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/enhanced/computer-use', methods=['POST'])
async def execute_computer_use():
    """Execute a computer use agent task"""
    try:
        data = request.json
        task_description = data.get('task_description')
        user_id = data.get('user_id', 'anonymous')
        
        # Submit as computer use task
        task_id = await mama_bear_orchestrator.submit_task(
            task_description=task_description,
            task_type=TaskType.COMPUTER_USE,
            user_id=user_id,
            priority=2
        )
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Computer use task started'
        })
        
    except Exception as e:
        logger.error(f"Computer use error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Enhanced Socket.IO events
@socketio.on('enhanced_task_progress')
async def handle_task_progress_request(data):
    """Handle real-time task progress requests"""
    try:
        task_id = data.get('task_id')
        if not task_id:
            emit('enhanced_task_error', {'error': 'Task ID required'})
            return
        
        status = await mama_bear_orchestrator.get_task_status(task_id)
        emit('enhanced_task_progress', status)
        
    except Exception as e:
        logger.error(f"Enhanced task progress error: {e}")
        emit('enhanced_task_error', {'error': str(e)})

# Template routes
@app.route('/monitoring')
def monitoring_page():
    """Monitoring dashboard page"""
    return render_template('monitoring.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': '🐻 This path doesn\'t exist in the sanctuary',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': '🐻 Something went wrong, but I\'m working on it!',
        'timestamp': datetime.now().isoformat()
    }), 500

# Startup function
async def startup():
    """Initialize all Mama Bear systems"""
    global mama_bear_system
    
    logger.info("🐻 Starting Podplay Sanctuary...")
    
    try:
        # Initialize the complete Mama Bear system
        mama_bear_system = await initialize_complete_system(app, socketio)
        
        logger.info("✅ Podplay Sanctuary is ready!")
        logger.info("🌟 Mama Bear is awake and ready to help Nathan!")
        
    except Exception as e:
        logger.error(f"❌ Failed to start Podplay Sanctuary: {e}")
        raise

# Shutdown function
async def shutdown():
    """Gracefully shutdown all systems"""
    global mama_bear_system
    
    logger.info("🐻 Shutting down Podplay Sanctuary...")
    
    if mama_bear_system:
        await mama_bear_system.shutdown()
    
    logger.info("✅ Podplay Sanctuary shutdown complete")

if __name__ == '__main__':
    # Run the startup sequence
    asyncio.run(startup())
    
    # Start the server
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )