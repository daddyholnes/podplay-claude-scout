"""
🐻 Podplay Sanctuary - Simplified Backend for Demo
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
from datetime import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mama-bear-sanctuary-secret'

# Enable CORS for all routes
CORS(app, origins=["*"])

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Mock data and state
mock_conversations = {}
connected_users = set()

# Mama Bear responses for demo
mama_bear_responses = {
    'main_chat': {
        'greeting': '🐻 Research Specialist Mama Bear here! I love diving deep into topics and discovering connections. What would you like to explore today?',
        'responses': [
            'That\'s a fascinating research question! Let me break this down into key areas we should investigate...',
            'Based on my research expertise, I can see several interesting angles to explore here...',
            'This reminds me of similar patterns I\'ve seen in other domains. Let me connect some dots for you...',
            'Great question! I\'ll need to dig deeper into the literature on this topic...'
        ]
    },
    'vm_hub': {
        'greeting': '🐻 DevOps Specialist Mama Bear reporting for duty! I\'ll keep your infrastructure running smoothly and securely.',
        'responses': [
            'I can help you set up that environment! Let me configure the optimal setup for your needs...',
            'That\'s a solid DevOps approach. I\'d recommend adding some monitoring and backup strategies...',
            'Perfect! I\'ll provision a new workspace with all the tools you need...',
            'Let me optimize those resource allocations for better performance...'
        ]
    },
    'scout': {
        'greeting': '🐻 Scout Commander Mama Bear ready for autonomous missions! Give me a task and I\'ll handle it from start to finish.',
        'responses': [
            'Excellent mission brief! I\'ll break this down into actionable steps and execute autonomously...',
            'This is exactly the kind of challenge I excel at! Let me plan the optimal approach...',
            'Mission accepted! I\'ll coordinate all the necessary resources and get this done...',
            'Perfect autonomous task! I\'ll handle everything and report back with results...'
        ]
    },
    'models': {
        'greeting': '🐻 Model Coordinator Mama Bear at your service! I know all the AI models and their strengths.',
        'responses': [
            'For this task, I recommend using Gemini Pro for the reasoning and Flash for speed...',
            'Great question about model selection! Each model has unique strengths...',
            'I can coordinate responses from multiple models to give you the best answer...',
            'Let me analyze which model would be optimal for your specific use case...'
        ]
    },
    'mcp': {
        'greeting': '🐻 Tool Curator Mama Bear here with endless enthusiasm for great tools! Let\'s find exactly what you need.',
        'responses': [
            'I found some amazing tools that would be perfect for your workflow!',
            'These MCP tools will supercharge your productivity! Let me show you...',
            'Perfect tool request! I have just the thing in our curated collection...',
            'I love discovering new tools! Here are some gems I think you\'ll appreciate...'
        ]
    },
    'integrations': {
        'greeting': '🐻 Integration Architect Mama Bear ready to build solid connections! Let\'s integrate it beautifully.',
        'responses': [
            'Excellent integration challenge! I\'ll design a robust, secure solution...',
            'That\'s a perfect use case for our integration patterns...',
            'I can build that connection with proper error handling and monitoring...',
            'Great integration idea! Let me architect a scalable solution...'
        ]
    },
    'live-api': {
        'greeting': '🐻 Live API Specialist Mama Bear energized for real-time magic! Let\'s make it responsive and amazing.',
        'responses': [
            'Real-time features are my specialty! I can optimize that for low latency...',
            'Perfect live API challenge! I\'ll make sure it\'s fast and reliable...',
            'I love working with real-time systems! Let me design something amazing...',
            'Great idea for a live feature! I\'ll implement it with proper streaming...'
        ]
    }
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'mama_bear': True,
            'memory': True,
            'scrapybara': True
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/mama-bear/chat', methods=['POST'])
def mama_bear_chat():
    """Main chat endpoint for Mama Bear interactions"""
    try:
        data = request.json
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'demo_user')
        
        # Simulate thinking time
        time.sleep(1)
        
        # Get appropriate response
        variant_responses = mama_bear_responses.get(page_context, mama_bear_responses['main_chat'])
        
        import random
        response = random.choice(variant_responses['responses'])
        
        # Add some context-specific responses
        if 'create' in message.lower() or 'build' in message.lower():
            response = f"🐻 I'd love to help you build that! {response}"
        elif 'help' in message.lower():
            response = f"🐻 Of course I can help! {response}"
        elif '?' in message:
            response = f"🐻 Great question! {response}"
        
        return jsonify({
            'success': True,
            'response': response,
            'metadata': {
                'model_used': 'mama_bear_demo',
                'variant': page_context,
                'processing_time': 1.0
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mama_bear_says': '🐻 I\'m having a small hiccup. Let me try again!'
        }), 500

@app.route('/api/mama-bear/status', methods=['GET'])
def mama_bear_status():
    """Get system status"""
    return jsonify({
        'success': True,
        'status': {
            'overall_health': 'healthy',
            'mama_bear_status': 'active',
            'variants_available': ['main_chat', 'vm_hub', 'scout', 'models', 'mcp', 'integrations', 'live-api'],
            'services': {
                'model_manager': {'overall_health': 'healthy'},
                'memory': {'connected': True},
                'scrapybara': {'available': True}
            },
            'capabilities': {
                'chat': True,
                'vision': True,
                'function_calling': True,
                'code_generation': True,
                'autonomous_tasks': True
            }
        },
        'timestamp': datetime.now().isoformat()
    })

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"🐻 Client connected: {request.sid}")
    connected_users.add(request.sid)
    emit('connected', {
        'message': '🐻 Welcome to Podplay Sanctuary! Mama Bear is here to help.',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"🐻 Client disconnected: {request.sid}")
    connected_users.discard(request.sid)

@socketio.on('join_page')
def handle_join_page(data):
    """Handle user joining a specific page"""
    page_context = data.get('page_context', 'main_chat')
    user_id = data.get('user_id', 'demo_user')
    
    print(f"🐻 User {user_id} joined {page_context}")
    
    # Get appropriate greeting
    variant_data = mama_bear_responses.get(page_context, mama_bear_responses['main_chat'])
    greeting = variant_data['greeting']
    
    emit('mama_bear_greeting', {
        'message': greeting,
        'variant': page_context,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('mama_bear_message')
def handle_mama_bear_message(data):
    """Handle real-time Mama Bear chat messages"""
    try:
        message = data.get('message', '')
        page_context = data.get('page_context', 'main_chat')
        user_id = data.get('user_id', 'demo_user')
        
        # Emit thinking status
        emit('mama_bear_thinking', {
            'thinking': True,
            'message': '🐻 Mama Bear is thinking...'
        })
        
        # Simulate processing time
        time.sleep(1.5)
        
        # Get response
        variant_responses = mama_bear_responses.get(page_context, mama_bear_responses['main_chat'])
        
        import random
        response = random.choice(variant_responses['responses'])
        
        # Add context to response
        if 'workspace' in message.lower() or 'vm' in message.lower():
            response = f"🐻 I'll set up a perfect workspace for you! {response}"
        elif 'integrate' in message.lower():
            response = f"🐻 Integration coming right up! {response}"
        elif 'research' in message.lower():
            response = f"🐻 I love research challenges! {response}"
        
        # Emit response
        emit('mama_bear_response', {
            'success': True,
            'response': response,
            'metadata': {
                'model_used': 'mama_bear_demo',
                'variant': page_context,
                'processing_time': 1.5
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"🐻 WebSocket error: {e}")
        emit('mama_bear_response', {
            'success': False,
            'error': str(e),
            'message': '🐻 I had a small hiccup! Let me try that again.'
        })

# Static file handlers
@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🐻</text></svg>''', 200, {'Content-Type': 'image/svg+xml'}

@app.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    return '''User-agent: *
Allow: /

# Podplay Sanctuary - AI Development Environment''', 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    """Serve basic sitemap"""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/vm-hub</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/scout</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/models</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/mcp</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/integrations</loc></url>
  <url><loc>https://8001-owoyqd-lnaafd.public.scrapybara.com/live-api</loc></url>
</urlset>''', 200, {'Content-Type': 'application/xml'}

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'mama_bear_says': '🐻 I can\'t find that path! Check the URL?'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'mama_bear_says': '🐻 Something went wrong, but I\'m on it!'
    }), 500

if __name__ == '__main__':
    print("🐻 Starting Podplay Sanctuary (Demo Mode)...")
    print("🌐 Frontend: https://8001-owoyqd-lnaafd.public.scrapybara.com")
    print("🔧 Backend: http://localhost:5000")
    print("✨ All Mama Bear variants ready!")
    
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        allow_unsafe_werkzeug=True
    )