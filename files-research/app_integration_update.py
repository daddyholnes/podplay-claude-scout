# app.py - Updated Integration for Enhanced Scrapybara Features
"""
🐻 Enhanced Podplay Sanctuary with Next-Level Mama Bear Capabilities
Integrates advanced Scrapybara features for computer control and collaboration
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json

# Initialize logging first
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'mama_bear.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PodplaySanctuary")

# Import existing sanctuary services
from config.settings import get_settings
from services import (
    initialize_all_services, 
    shutdown_all_services,
    get_mama_bear_agent,
    get_memory_manager, 
    get_scrapybara_manager,
    get_theme_manager,
    get_service_status
)

# Import enhanced Mama Bear orchestration
try:
    from services.mama_bear_orchestration import AgentOrchestrator
    from services.mama_bear_workflow_logic import initialize_workflow_intelligence, create_collaboration_orchestrator
    from services.mama_bear_memory_system import initialize_enhanced_memory
    ENHANCED_ORCHESTRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced orchestration not available: {e}")
    ENHANCED_ORCHESTRATION_AVAILABLE = False

# Import enhanced Scrapybara integration
try:
    from services.enhanced_scrapybara_integration import (
        create_enhanced_scrapybara_manager,
        integrate_with_mama_bear_agents,
        EnhancedScrapybaraManager
    )
    from api.enhanced_scrapybara_api import integrate_enhanced_scrapybara_api
    ENHANCED_SCRAPYBARA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced Scrapybara integration not available: {e}")
    ENHANCED_SCRAPYBARA_AVAILABLE = False

# Import API integration
try:
    from api.mama_bear_orchestration_api import integrate_orchestration_with_app
    API_INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"API integration not available: {e}")
    API_INTEGRATION_AVAILABLE = False

# Try to import Mem0 for enhanced memory
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    MemoryClient = None

# Initialize Flask app
app = Flask(__name__)
settings = get_settings()
app.config['SECRET_KEY'] = settings.flask_secret_key
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"])

# Initialize SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"],
    async_mode='threading'
)

# Global service status
services_initialized = False
mama_bear_orchestrator = None
enhanced_scrapybara_manager = None

async def initialize_sanctuary_services():
    """Initialize all sanctuary services including enhanced Scrapybara features"""
    global services_initialized, mama_bear_orchestrator, enhanced_scrapybara_manager
    
    try:
        logger.info("🚀 Initializing Enhanced Podplay Sanctuary services...")
        
        # Initialize basic services through the service manager
        await initialize_all_services()
        
        # Initialize enhanced Scrapybara integration if available
        if ENHANCED_SCRAPYBARA_AVAILABLE:
            logger.info("🌐 Initializing Enhanced Scrapybara Integration...")
            
            # Create enhanced Scrapybara manager
            enhanced_scrapybara_config = {
                'scrapybara_api_key': os.getenv('SCRAPYBARA_API_KEY'),
                'scrapybara_base_url': os.getenv('SCRAPYBARA_BASE_URL', 'https://api.scrapybara.com/v1'),
                'enable_cua': True,  # Enable Computer Use Agent
                'enable_collaboration': True,
                'enable_auth_flows': True,
                'max_concurrent_instances': int(os.getenv('SCRAPYBARA_MAX_INSTANCES', '10')),
                'permission_level': os.getenv('SCRAPYBARA_PERMISSION_LEVEL', 'elevated')
            }
            
            enhanced_scrapybara_manager = await create_enhanced_scrapybara_manager(enhanced_scrapybara_config)
            
            # Store globally for API access
            app.enhanced_scrapybara_manager = enhanced_scrapybara_manager
            
            logger.info("✅ Enhanced Scrapybara Manager initialized with:")
            logger.info("  🌐 Shared browser sessions")
            logger.info("  🤖 Computer Use Agent control")
            logger.info("  🔐 Authenticated web sessions")
            logger.info("  🔍 Multi-instance research environments")
            logger.info("  🤝 Real-time collaboration")
        
        # Initialize enhanced Mama Bear orchestration if available
        if ENHANCED_ORCHESTRATION_AVAILABLE:
            logger.info("🐻 Initializing Enhanced Mama Bear Orchestration...")
            
            # Initialize Mem0 if available
            mem0_client = None
            if MEM0_AVAILABLE and MemoryClient:
                try:
                    mem0_client = MemoryClient()
                    logger.info("✅ Mem0 client initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize Mem0: {e}")
                    mem0_client = None
            
            # Initialize enhanced memory system
            enhanced_memory = None
            if initialize_enhanced_memory:
                enhanced_memory = await initialize_enhanced_memory(
                    mem0_client=mem0_client,
                    config={
                        'memory_storage_path': './mama_bear_memory',
                        'cleanup_on_startup': True,
                        'memory_retention_days': 90
                    }
                )
            
            # Initialize workflow intelligence
            workflow_intelligence = None
            if initialize_workflow_intelligence:
                workflow_intelligence = await initialize_workflow_intelligence()
            
            # Initialize orchestrator with enhanced components
            if AgentOrchestrator:
                mama_bear_orchestrator = AgentOrchestrator(
                    memory_manager=get_memory_manager(),
                    model_manager=get_mama_bear_agent(),
                    scrapybara_client=enhanced_scrapybara_manager or get_scrapybara_manager(),
                    enhanced_memory=enhanced_memory,
                    workflow_intelligence=workflow_intelligence,
                    mem0_client=mem0_client
                )
                
                # Store orchestrator globally
                app.mama_bear_orchestrator = mama_bear_orchestrator
                
                # Integrate enhanced Scrapybara capabilities with Mama Bear agents
                if ENHANCED_SCRAPYBARA_AVAILABLE and enhanced_scrapybara_manager:
                    await integrate_with_mama_bear_agents(enhanced_scrapybara_manager, mama_bear_orchestrator)
                    logger.info("🔗 Enhanced Scrapybara capabilities integrated with Mama Bear agents!")
            
            # Integrate API endpoints if available
            if API_INTEGRATION_AVAILABLE and integrate_orchestration_with_app:
                integrate_orchestration_with_app(app, socketio)
                logger.info("✅ Enhanced orchestration API integrated")
            
            logger.info("✅ Enhanced Mama Bear Orchestration initialized")
        
        # Integrate enhanced Scrapybara API endpoints
        if ENHANCED_SCRAPYBARA_AVAILABLE:
            integrate_enhanced_scrapybara_api(app, socketio)
            logger.info("✅ Enhanced Scrapybara API endpoints integrated")
        
        services_initialized = True
        
        logger.info("✅ All enhanced sanctuary services initialized successfully")
        logger.info("🐻 Enhanced Mama Bear with next-level capabilities is ready!")
        logger.info("🌟 Features available:")
        logger.info("  • Intelligent agent orchestration")
        logger.info("  • Shared browser sessions with real-time collaboration")
        logger.info("  • Computer Use Agent for desktop automation")
        logger.info("  • Authenticated web session management")
        logger.info("  • Multi-instance research environments")
        logger.info("  • Persistent memory with Mem0 integration")
        logger.info("  • Advanced workflow intelligence")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize enhanced services: {str(e)}")
        # Don't raise - allow basic services to work
        services_initialized = True
        logger.info("⚠️ Running with basic services only")

def get_service_instances():
    """Get all service instances including enhanced ones"""
    if not services_initialized:
        raise RuntimeError("Services not initialized. Call initialize_sanctuary_services() first.")
    
    instances = {
        'mama_bear': get_mama_bear_agent(),
        'memory': get_memory_manager(),
        'scrapybara': get_scrapybara_manager(),
        'theme': get_theme_manager()
    }
    
    # Add enhanced services if available
    if enhanced_scrapybara_manager:
        instances['enhanced_scrapybara'] = enhanced_scrapybara_manager
    
    if mama_bear_orchestrator:
        instances['orchestrator'] = mama_bear_orchestrator
    
    return instances

# ==============================================================================
# ENHANCED MAMA BEAR ENDPOINTS (keeping existing ones + new integration info)
# ==============================================================================

@app.route('/api/mama-bear/chat', methods=['POST'])
async def mama_bear_chat():
    """Main chat endpoint with enhanced routing to specialized agents"""
    try:
        services = get_service_instances()
        
        data = request.json or {}
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'nathan_sanctuary')
        attachments = data.get('attachments', [])
        
        # Use orchestrator if available for intelligent routing
        if 'orchestrator' in services:
            orchestrator = services['orchestrator']
            response = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            return jsonify({
                'success': True,
                'response': response.get('message', response.get('content', str(response))),
                'agent_used': response.get('agent', 'orchestrated'),
                'workflow_type': response.get('type', 'standard'),
                'model_used': response.get('model_used', 'orchestrated'),
                'enhanced_features_used': True,
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Fallback to basic Mama Bear
            mama_bear = services['mama_bear']
            response = await mama_bear.process_message(
                message=message,
                page_context=page_context,
                user_id=user_id,
                attachments=attachments
            )
            
            return jsonify({
                'success': True,
                'response': response['content'],
                'variant_used': response['variant'],
                'model_used': response['model'],
                'enhanced_features_used': False,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Error in mama_bear_chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🐻 I'm experiencing some technical difficulties, but I'm working on it!"
        }), 500

@app.route('/api/mama-bear/capabilities', methods=['GET'])
def get_mama_bear_capabilities():
    """Get information about available Mama Bear capabilities"""
    try:
        services = get_service_instances()
        
        capabilities = {
            'basic_chat': True,
            'memory_management': 'memory' in services,
            'theme_management': 'theme' in services,
            'vm_management': 'scrapybara' in services,
            'enhanced_orchestration': 'orchestrator' in services,
            'enhanced_scrapybara': 'enhanced_scrapybara' in services,
        }
        
        # Enhanced capabilities if available
        enhanced_features = {}
        if 'enhanced_scrapybara' in services:
            enhanced_features.update({
                'shared_browser_sessions': True,
                'computer_use_agent': True,
                'authenticated_sessions': True,
                'multi_instance_research': True,
                'real_time_collaboration': True,
                'advanced_automation': True
            })
        
        if 'orchestrator' in services:
            enhanced_features.update({
                'intelligent_agent_routing': True,
                'workflow_intelligence': True,
                'agent_collaboration': True,
                'persistent_memory': True,
                'decision_patterns': True
            })
        
        return jsonify({
            'success': True,
            'capabilities': capabilities,
            'enhanced_features': enhanced_features,
            'agent_count': len(getattr(services.get('orchestrator'), 'agents', {})),
            'system_version': '2.0-enhanced',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# ENHANCED SYSTEM STATUS AND HEALTH ENDPOINTS
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check with detailed service status"""
    try:
        basic_status = get_service_status()
        
        # Add enhanced service status
        enhanced_status = {}
        
        if enhanced_scrapybara_manager:
            enhanced_status['enhanced_scrapybara'] = {
                'status': 'healthy',
                'shared_sessions': len(enhanced_scrapybara_manager.shared_sessions),
                'authenticated_sessions': len(enhanced_scrapybara_manager.authenticated_sessions),
                'active_instances': len(enhanced_scrapybara_manager.instances)
            }
        
        if mama_bear_orchestrator:
            enhanced_status['orchestrator'] = {
                'status': 'healthy',
                'active_agents': len(mama_bear_orchestrator.agents),
                'active_tasks': len(getattr(mama_bear_orchestrator, 'active_tasks', {})),
                'collaboration_sessions': len(getattr(mama_bear_orchestrator, 'collaboration_sessions', {}))
            }
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'services': {**basic_status, **enhanced_status},
            'enhanced_features_active': len(enhanced_status) > 0,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ==============================================================================
# ENHANCED WEBSOCKET HANDLERS
# ==============================================================================

@socketio.on('connect')
def handle_connect():
    """Enhanced connection handler with feature detection"""
    logger.info("Client connected")
    
    # Detect available features
    enhanced_features = {
        'orchestration': mama_bear_orchestrator is not None,
        'enhanced_scrapybara': enhanced_scrapybara_manager is not None,
        'shared_browser': enhanced_scrapybara_manager is not None,
        'computer_control': enhanced_scrapybara_manager is not None,
        'real_time_collaboration': True
    }
    
    emit('connection_established', {
        'status': 'connected',
        'sanctuary_version': '2.0-enhanced',
        'mama_bear_ready': True,
        'enhanced_features': enhanced_features,
        'message': '🐻 Enhanced Mama Bear Sanctuary is ready! New capabilities unlocked! 🚀'
    })

@socketio.on('mama_bear_message')
async def handle_mama_bear_message(data):
    """Enhanced real-time Mama Bear message handler"""
    try:
        services = get_service_instances()
        
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'nathan_sanctuary')
        
        # Use orchestrator if available
        if 'orchestrator' in services:
            orchestrator = services['orchestrator']
            
            # Emit thinking status
            emit('mama_bear_thinking', {
                'status': 'analyzing',
                'message': '🧠 Analyzing with enhanced intelligence...',
                'agent_routing': True
            })
            
            response = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            # Emit enhanced response
            emit('mama_bear_response', {
                'content': response.get('message', response.get('content', str(response))),
                'agent_used': response.get('agent', 'orchestrated'),
                'workflow_type': response.get('type', 'standard'),
                'model_used': response.get('model_used', 'orchestrated'),
                'enhanced': True,
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Fallback to basic processing
            mama_bear = services['mama_bear']
            
            emit('mama_bear_thinking', {
                'status': 'processing',
                'message': '🐻 Mama Bear is thinking...'
            })
            
            response = await mama_bear.process_message(
                message=message,
                page_context=page_context,
                user_id=user_id
            )
            
            emit('mama_bear_response', {
                'content': response['content'],
                'variant': response['variant'],
                'model': response['model'],
                'enhanced': False,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Error in WebSocket message handler: {str(e)}")
        emit('error', {
            'message': str(e),
            'fallback': '🐻 Something went wrong, but I\'m still here to help!'
        })

# Keep all existing endpoints from the original app.py...
# (VM endpoints, Scout endpoints, Theme endpoints, Memory endpoints, etc.)

# ==============================================================================
# APPLICATION STARTUP WITH ENHANCED FEATURES
# ==============================================================================

def create_app():
    """Enhanced application factory function"""
    # Initialize services when app is created
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initialize_sanctuary_services())
    
    return app

if __name__ == '__main__':
    # Initialize services
    import asyncio
    
    async def startup():
        """Enhanced async startup function"""
        logger.info("🚀 Starting Enhanced Podplay Sanctuary...")
        await initialize_sanctuary_services()
        
        if enhanced_scrapybara_manager and mama_bear_orchestrator:
            logger.info("🌟 Enhanced Mama Bear is ready with next-level capabilities!")
            logger.info("  • Shared browser sessions for real-time collaboration")
            logger.info("  • Computer Use Agent for desktop automation")
            logger.info("  • Intelligent agent orchestration and routing")
            logger.info("  • Authenticated web session management")
            logger.info("  • Multi-instance research environments")
            logger.info("  • Advanced workflow intelligence")
        else:
            logger.info("🐻 Basic Mama Bear is ready!")
    
    # Run startup
    asyncio.run(startup())
    
    # Start the Enhanced Sanctuary
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('BACKEND_PORT', 5001)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )