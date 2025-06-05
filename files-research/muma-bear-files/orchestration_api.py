# backend/api/mama_bear_orchestration_api.py
"""
🐻 Mama Bear Orchestration API
RESTful endpoints and WebSocket handlers for agent coordination
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Blueprint for REST endpoints
orchestration_bp = Blueprint('orchestration', __name__)

@orchestration_bp.route('/api/mama-bear/chat', methods=['POST'])
async def intelligent_chat():
    """
    🐻 Main chat endpoint with intelligent agent routing
    Automatically determines which agents to involve based on the request
    """
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        
        # Get orchestrator from app
        orchestrator = current_app.mama_bear_orchestrator
        
        # Process the request with intelligent routing
        result = await orchestrator.process_user_request(
            message=message,
            user_id=user_id,
            page_context=page_context
        )
        
        return jsonify({
            'success': True,
            'response': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in intelligent_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🐻 I'm having a moment! Let me gather myself and try again."
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/status', methods=['GET'])
async def get_agents_status():
    """Get status of all agents"""
    try:
        orchestrator = current_app.mama_bear_orchestrator
        status = await orchestrator.get_system_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/agents/<agent_id>/direct', methods=['POST'])
async def direct_agent_communication():
    """Communicate directly with a specific agent"""
    try:
        agent_id = request.view_args['agent_id']
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = current_app.mama_bear_orchestrator
        
        # Get the specific agent
        agent = orchestrator.agents.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not found'
            }), 404
        
        # Direct communication with agent
        result = await agent.handle_request(message, user_id)
        
        return jsonify({
            'success': True,
            'response': result,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/plans', methods=['POST'])
async def create_plan():
    """Create a new plan for complex requests"""
    try:
        data = request.json
        request_text = data.get('request', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = current_app.mama_bear_orchestrator
        lead_developer = orchestrator.agents.get('lead_developer')
        
        plan = await lead_developer.create_plan(request_text, user_id)
        
        return jsonify({
            'success': True,
            'plan': plan,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/plans/<plan_id>/execute', methods=['POST'])
async def execute_plan():
    """Execute an approved plan"""
    try:
        plan_id = request.view_args['plan_id']
        
        # Plan execution logic would go here
        # For now, return a placeholder
        
        return jsonify({
            'success': True,
            'message': f'Plan {plan_id} execution started',
            'execution_id': f'exec_{datetime.now().timestamp()}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['GET'])
async def get_global_context():
    """Get current global context"""
    try:
        orchestrator = current_app.mama_bear_orchestrator
        
        return jsonify({
            'success': True,
            'context': orchestrator.context_awareness.global_context,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/mama-bear/context', methods=['POST'])
async def update_global_context():
    """Update global context"""
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({
                'success': False,
                'error': 'Key is required'
            }), 400
        
        orchestrator = current_app.mama_bear_orchestrator
        await orchestrator.context_awareness.update_global_context(key, value)
        
        return jsonify({
            'success': True,
            'message': f'Context updated: {key}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket handlers for real-time communication
def init_socketio_handlers(socketio):
    """Initialize WebSocket handlers for orchestration"""
    
    @socketio.on('join_orchestration')
    def on_join_orchestration(data):
        """Join orchestration room for real-time updates"""
        user_id = data.get('user_id', 'anonymous')
        join_room(f'orchestration_{user_id}')
        emit('joined_orchestration', {
            'status': 'Connected to Mama Bear Orchestration',
            'user_id': user_id
        })
    
    @socketio.on('mama_bear_chat_realtime')
    async def handle_realtime_chat(data):
        """Handle real-time chat with agent orchestration"""
        try:
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            page_context = data.get('page_context', 'main_chat')
            
            # Join user's room for updates
            join_room(f'orchestration_{user_id}')
            
            # Emit thinking status
            emit('mama_bear_thinking', {
                'status': 'analyzing_request',
                'message': '🐻 Let me think about the best way to help you...'
            }, room=f'orchestration_{user_id}')
            
            # Get orchestrator
            orchestrator = current_app.mama_bear_orchestrator
            
            # Process with orchestration
            result = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            # Emit the result
            emit('mama_bear_response', {
                'success': True,
                'response': result,
                'timestamp': datetime.now().isoformat()
            }, room=f'orchestration_{user_id}')
            
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            emit('mama_bear_error', {
                'success': False,
                'error': str(e),
                'fallback_message': "🐻 Something went wrong, but I'm here to help!"
            }, room=f'orchestration_{user_id}')
    
    @socketio.on('get_agent_status')
    async def handle_agent_status_request():
        """Get real-time agent status"""
        try:
            orchestrator = current_app.mama_bear_orchestrator
            status = await orchestrator.get_system_status()
            
            emit('agent_status_update', {
                'success': True,
                'status': status,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            emit('agent_status_error', {
                'success': False,
                'error': str(e)
            })
    
    @socketio.on('send_agent_message')
    async def handle_inter_agent_message(data):
        """Handle messages between agents"""
        try:
            from_agent = data.get('from_agent')
            to_agent = data.get('to_agent')
            message = data.get('message')
            context = data.get('context', {})
            
            orchestrator = current_app.mama_bear_orchestrator
            await orchestrator.send_agent_message(from_agent, to_agent, message, context)
            
            emit('agent_message_sent', {
                'success': True,
                'from': from_agent,
                'to': to_agent,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            emit('agent_message_error', {
                'success': False,
                'error': str(e)
            })
    
    @socketio.on('start_collaboration')
    async def handle_collaboration_start(data):
        """Start a collaboration session"""
        try:
            agents = data.get('agents', [])
            task_description = data.get('task_description', '')
            user_id = data.get('user_id', 'default_user')
            
            # Emit collaboration started
            emit('collaboration_started', {
                'collaboration_id': f'collab_{datetime.now().timestamp()}',
                'agents': agents,
                'status': 'initializing',
                'timestamp': datetime.now().isoformat()
            }, room=f'orchestration_{user_id}')
            
            # The actual collaboration logic would be handled by the orchestrator
            # This is just the WebSocket interface
            
        except Exception as e:
            emit('collaboration_error', {
                'success': False,
                'error': str(e)
            })

# Background task for broadcasting system updates
async def system_monitor_broadcast(app, socketio):
    """Background task to broadcast system status updates"""
    
    while True:
        try:
            with app.app_context():
                if hasattr(app, 'mama_bear_orchestrator'):
                    orchestrator = app.mama_bear_orchestrator
                    status = await orchestrator.get_system_status()
                    
                    # Broadcast to all connected clients
                    socketio.emit('system_status_update', {
                        'status': status,
                        'timestamp': datetime.now().isoformat()
                    }, namespace='/', broadcast=True)
            
            # Wait 30 seconds before next update
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"System monitor broadcast error: {e}")
            await asyncio.sleep(60)  # Wait longer on error

# Enhanced Flask app integration
def integrate_orchestration_with_app(app, socketio, memory_manager, model_manager, scrapybara_client):
    """
    Complete integration of orchestration system with Flask app
    """
    
    # Initialize orchestration
    async def init_orchestration():
        from mama_bear_orchestration import initialize_orchestration
        orchestrator = await initialize_orchestration(
            app, memory_manager, model_manager, scrapybara_client
        )
        return orchestrator
    
    # Register blueprint
    app.register_blueprint(orchestration_bp)
    
    # Initialize WebSocket handlers
    init_socketio_handlers(socketio)
    
    # Start background monitoring
    with app.app_context():
        asyncio.create_task(init_orchestration())
        asyncio.create_task(system_monitor_broadcast(app, socketio))
    
    # Add middleware for context preservation
    @app.before_request
    def before_request():
        """Preserve context across requests"""
        if hasattr(app, 'mama_bear_orchestrator') and request.json:
            user_id = request.json.get('user_id')
            if user_id:
                # Update last activity for user
                asyncio.create_task(
                    app.mama_bear_orchestrator.context_awareness.update_global_context(
                        'last_user_activity', 
                        {'user_id': user_id, 'timestamp': datetime.now()}
                    )
                )
    
    logger.info("🐻 Mama Bear Orchestration API integrated successfully!")

# Example usage in main app.py
"""
from api.mama_bear_orchestration_api import integrate_orchestration_with_app

# In your create_app function:
def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize your existing services
    memory_manager = MemoryManager()
    model_manager = MamaBearModelManager()
    scrapybara_client = Scrapybara()
    
    # Integrate orchestration
    integrate_orchestration_with_app(
        app, socketio, memory_manager, model_manager, scrapybara_client
    )
    
    return app, socketio
"""