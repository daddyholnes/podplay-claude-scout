# backend/api/enhanced_scrapybara_api.py
"""
🐻 Enhanced Scrapybara API Endpoints
RESTful and WebSocket endpoints for advanced browser control and computer use
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
from datetime import datetime
import logging
import uuid

from services.enhanced_scrapybara_integration import (
    ComputerActionRequest, 
    ComputerAction,
    EnhancedScrapybaraManager
)

logger = logging.getLogger(__name__)

# Blueprint for enhanced Scrapybara endpoints
enhanced_scrapybara_bp = Blueprint('enhanced_scrapybara', __name__)

def get_scrapybara_manager() -> EnhancedScrapybaraManager:
    """Safely get enhanced Scrapybara manager from app context"""
    return getattr(current_app, 'enhanced_scrapybara_manager', None)

# ==============================================================================
# SHARED BROWSER SESSION ENDPOINTS
# ==============================================================================

@enhanced_scrapybara_bp.route('/api/scrapybara/shared-browser/start', methods=['POST'])
async def start_shared_browser_session():
    """🌐 Start shared browser session with Mama Bear"""
    try:
        data = request.json or {}
        user_id = data.get('user_id', 'default_user')
        agent_id = data.get('agent_id', 'research_specialist')
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Start shared session
        session = await manager.start_shared_browser_session(user_id, agent_id)
        
        return jsonify({
            'success': True,
            'session': {
                'session_id': session.session_id,
                'browser_url': session.browser_url,
                'websocket_url': session.websocket_url,
                'instance_id': session.instance_id,
                'participants': session.participants,
                'permissions': session.permissions
            },
            'message': '🌐 Shared browser session started! You and Mama Bear can now collaborate in real-time.',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error starting shared browser session: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': '🐻 Having trouble starting the shared session. Let me try a different approach!'
        }), 500

@enhanced_scrapybara_bp.route('/api/scrapybara/shared-browser/<session_id>/status', methods=['GET'])
async def get_shared_session_status(session_id):
    """Get status of shared browser session"""
    try:
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({'success': False, 'error': 'Manager not available'}), 500
        
        if session_id not in manager.shared_sessions:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        session = manager.shared_sessions[session_id]
        
        return jsonify({
            'success': True,
            'session': {
                'session_id': session.session_id,
                'status': 'active',
                'participants': session.participants,
                'current_url': session.current_url,
                'last_activity': session.last_activity.isoformat(),
                'collaboration_enabled': session.collaboration_enabled
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==============================================================================
# COMPUTER USE AGENT ENDPOINTS
# ==============================================================================

@enhanced_scrapybara_bp.route('/api/scrapybara/computer-control/execute', methods=['POST'])
async def execute_computer_action():
    """🤖 Execute computer control action"""
    try:
        data = request.json or {}
        
        # Create action request
        action_request = ComputerActionRequest(
            action_id=str(uuid.uuid4()),
            action_type=ComputerAction(data.get('action_type', 'click')),
            target=data.get('target', {}),
            parameters=data.get('parameters', {}),
            user_id=data.get('user_id', 'default_user'),
            permission_level=data.get('permission_level', 'restricted')
        )
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Execute action
        result = await manager.execute_computer_action(action_request)
        
        return jsonify({
            'success': result.get('success', False),
            'action_id': action_request.action_id,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error executing computer action: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_scrapybara_bp.route('/api/scrapybara/computer-control/workflow', methods=['POST'])
async def create_computer_workflow():
    """🔧 Create and execute computer control workflow"""
    try:
        data = request.json or {}
        workflow_description = data.get('workflow_description', '')
        user_id = data.get('user_id', 'default_user')
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Create workflow
        result = await manager.create_computer_control_workflow(
            workflow_description, 
            user_id
        )
        
        return jsonify({
            'success': result.get('success', False),
            'workflow': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating computer workflow: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# AUTHENTICATION MANAGEMENT ENDPOINTS
# ==============================================================================

@enhanced_scrapybara_bp.route('/api/scrapybara/auth/login', methods=['POST'])
async def login_to_service():
    """🔐 Authenticate to external service"""
    try:
        data = request.json or {}
        service_name = data.get('service_name', '')
        user_id = data.get('user_id', 'default_user')
        credentials_vault_key = data.get('credentials_vault_key', '')
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Authenticate to service
        result = await manager.login_to_service(
            service_name, 
            user_id, 
            credentials_vault_key
        )
        
        return jsonify({
            'success': result.get('success', False),
            'authentication': result,
            'message': f'🔐 Authentication to {service_name} {"successful" if result.get("success") else "failed"}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error authenticating to service: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_scrapybara_bp.route('/api/scrapybara/auth/sessions', methods=['GET'])
async def get_authenticated_sessions():
    """Get list of authenticated sessions"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({'success': False, 'error': 'Manager not available'}), 500
        
        # Get user's authenticated sessions
        user_sessions = {
            key: session for key, session in manager.authenticated_sessions.items()
            if session['user_id'] == user_id
        }
        
        return jsonify({
            'success': True,
            'sessions': user_sessions,
            'session_count': len(user_sessions)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==============================================================================
# RESEARCH ENVIRONMENT ENDPOINTS
# ==============================================================================

@enhanced_scrapybara_bp.route('/api/scrapybara/research/environment', methods=['POST'])
async def create_research_environment():
    """🔍 Create dedicated research environment"""
    try:
        data = request.json or {}
        research_topic = data.get('research_topic', '')
        user_id = data.get('user_id', 'default_user')
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Create research environment
        result = await manager.create_research_environment(research_topic, user_id)
        
        return jsonify({
            'success': result.get('success', False),
            'research_environment': result,
            'message': f'🔍 Research environment for "{research_topic}" {"created" if result.get("success") else "failed"}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating research environment: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_scrapybara_bp.route('/api/scrapybara/research/execute', methods=['POST'])
async def execute_collaborative_research():
    """🧠 Execute collaborative research with multiple queries"""
    try:
        data = request.json or {}
        research_queries = data.get('research_queries', [])
        user_id = data.get('user_id', 'default_user')
        
        if not research_queries:
            return jsonify({
                'success': False,
                'error': 'No research queries provided'
            }), 400
        
        manager = get_scrapybara_manager()
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Enhanced Scrapybara manager not available'
            }), 500
        
        # Execute collaborative research
        result = await manager.execute_collaborative_research(research_queries, user_id)
        
        return jsonify({
            'success': result.get('success', False),
            'research_results': result,
            'message': f'🧠 Collaborative research completed with {len(research_queries)} queries',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error executing collaborative research: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# INTEGRATION WITH MAMA BEAR AGENTS
# ==============================================================================

@enhanced_scrapybara_bp.route('/api/scrapybara/agents/enhance', methods=['POST'])
async def enhance_mama_bear_agents():
    """🔗 Enhance Mama Bear agents with advanced Scrapybara capabilities"""
    try:
        data = request.json or {}
        agent_ids = data.get('agent_ids', ['scout_commander', 'research_specialist'])
        
        manager = get_scrapybara_manager()
        orchestrator = getattr(current_app, 'mama_bear_orchestrator', None)
        
        if not manager or not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Required components not available'
            }), 500
        
        # Import integration function
        from services.enhanced_scrapybara_integration import integrate_with_mama_bear_agents
        
        # Enhance agents
        await integrate_with_mama_bear_agents(manager, orchestrator)
        
        return jsonify({
            'success': True,
            'enhanced_agents': agent_ids,
            'message': '🔗 Mama Bear agents enhanced with advanced capabilities!',
            'capabilities_added': [
                'Computer control',
                'Shared browser sessions',
                'Authenticated web sessions',
                'Collaborative research',
                'Multi-instance orchestration'
            ],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error enhancing Mama Bear agents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# WEBSOCKET HANDLERS FOR REAL-TIME COLLABORATION
# ==============================================================================

def setup_enhanced_scrapybara_websockets(socketio):
    """Setup WebSocket handlers for enhanced Scrapybara features"""
    
    @socketio.on('join_shared_browser')
    def on_join_shared_browser(data):
        """Join shared browser session room"""
        data = data or {}
        session_id = data.get('session_id')
        user_id = data.get('user_id', 'default_user')
        
        if session_id:
            room = f"shared_browser_{session_id}"
            join_room(room)
            
            emit('joined_shared_browser', {
                'session_id': session_id,
                'room': room,
                'status': 'connected',
                'message': '🌐 Connected to shared browser session'
            })
            
            # Notify other participants
            socketio.emit('participant_joined', {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }, to=room, include_self=False)
            
            logger.info(f"🌐 User {user_id} joined shared browser session {session_id}")
    
    @socketio.on('leave_shared_browser')
    def on_leave_shared_browser(data):
        """Leave shared browser session room"""
        data = data or {}
        session_id = data.get('session_id')
        user_id = data.get('user_id', 'default_user')
        
        if session_id:
            room = f"shared_browser_{session_id}"
            leave_room(room)
            
            # Notify other participants
            socketio.emit('participant_left', {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }, to=room)
            
            emit('left_shared_browser', {
                'session_id': session_id,
                'status': 'disconnected'
            })
    
    @socketio.on('shared_browser_action')
    async def on_shared_browser_action(data):
        """Handle shared browser actions"""
        try:
            data = data or {}
            session_id = data.get('session_id')
            action_type = data.get('action_type')
            action_data = data.get('action_data', {})
            user_id = data.get('user_id', 'default_user')
            
            room = f"shared_browser_{session_id}"
            
            # Get manager
            manager = get_scrapybara_manager()
            if not manager:
                emit('shared_browser_error', {
                    'error': 'Manager not available'
                })
                return
            
            # Execute action based on type
            if action_type == 'navigate':
                # Sync navigation across all participants
                socketio.emit('browser_navigation', {
                    'url': action_data.get('url'),
                    'initiated_by': user_id,
                    'timestamp': datetime.now().isoformat()
                }, to=room)
                
            elif action_type == 'cursor_move':
                # Sync cursor position
                socketio.emit('cursor_sync', {
                    'position': action_data.get('position', {'x': 0, 'y': 0}),
                    'user_id': user_id
                }, to=room, include_self=False)
                
            elif action_type == 'scroll':
                # Sync scroll position
                socketio.emit('scroll_sync', {
                    'position': action_data.get('position', {'x': 0, 'y': 0}),
                    'initiated_by': user_id
                }, to=room, include_self=False)
            
            elif action_type == 'mama_bear_suggestion':
                # Mama Bear suggests next action
                suggestion = action_data.get('suggestion', '')
                socketio.emit('mama_bear_suggests', {
                    'suggestion': suggestion,
                    'action_options': action_data.get('options', []),
                    'confidence': action_data.get('confidence', 0.8),
                    'timestamp': datetime.now().isoformat()
                }, to=room)
        
        except Exception as e:
            emit('shared_browser_error', {
                'error': str(e),
                'action_type': action_type
            })
    
    @socketio.on('computer_control_request')
    async def on_computer_control_request(data):
        """Handle computer control requests via WebSocket"""
        try:
            data = data or {}
            user_id = data.get('user_id', 'default_user')
            action_description = data.get('action_description', '')
            permission_level = data.get('permission_level', 'restricted')
            
            room = f"user_{user_id}"
            
            # Emit processing status
            emit('computer_control_status', {
                'status': 'processing',
                'message': '🤖 Mama Bear is analyzing your request...'
            })
            
            manager = get_scrapybara_manager()
            if not manager:
                emit('computer_control_error', {
                    'error': 'Manager not available'
                })
                return
            
            # Create workflow
            result = await manager.create_computer_control_workflow(
                action_description, 
                user_id
            )
            
            # Emit result
            emit('computer_control_result', {
                'success': result.get('success', False),
                'workflow': result,
                'message': '🤖 Computer control workflow executed!',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            emit('computer_control_error', {
                'error': str(e),
                'message': '🐻 Had trouble with that computer control request'
            })
    
    @socketio.on('research_collaboration_start')
    async def on_research_collaboration_start(data):
        """Start collaborative research session"""
        try:
            data = data or {}
            user_id = data.get('user_id', 'default_user')
            research_topic = data.get('research_topic', '')
            queries = data.get('queries', [])
            
            room = f"research_{user_id}"
            join_room(room)
            
            # Emit progress updates
            emit('research_progress', {
                'status': 'initializing',
                'message': f'🔍 Setting up research environment for "{research_topic}"...',
                'progress': 10
            })
            
            manager = get_scrapybara_manager()
            if not manager:
                emit('research_error', {'error': 'Manager not available'})
                return
            
            # Create research environment
            env_result = await manager.create_research_environment(research_topic, user_id)
            
            emit('research_progress', {
                'status': 'environment_ready',
                'message': '🔍 Research environment created!',
                'progress': 30,
                'environment': env_result
            })
            
            # Execute research if queries provided
            if queries:
                emit('research_progress', {
                    'status': 'executing_queries',
                    'message': f'🧠 Executing {len(queries)} research queries...',
                    'progress': 50
                })
                
                research_result = await manager.execute_collaborative_research(queries, user_id)
                
                emit('research_complete', {
                    'status': 'completed',
                    'message': '🎉 Collaborative research completed!',
                    'progress': 100,
                    'results': research_result
                })
            
        except Exception as e:
            emit('research_error', {
                'error': str(e),
                'message': '🐻 Encountered an issue during research setup'
            })


def integrate_enhanced_scrapybara_api(app, socketio):
    """Integrate enhanced Scrapybara API with Flask app"""
    
    # Register blueprint
    app.register_blueprint(enhanced_scrapybara_bp)
    
    # Setup WebSocket handlers
    setup_enhanced_scrapybara_websockets(socketio)
    
    logger.info("🚀 Enhanced Scrapybara API integrated successfully!")
    logger.info("Available features:")
    logger.info("  🌐 Shared browser sessions")
    logger.info("  🤖 Computer Use Agent control")
    logger.info("  🔐 Authenticated web sessions")
    logger.info("  🔍 Multi-instance research environments")
    logger.info("  🤝 Real-time collaboration")
