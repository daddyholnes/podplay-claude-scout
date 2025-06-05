# 🐻 Enhanced Mama Bear Integration Guide

## Complete Setup for Next-Level Browser Control & Computer Use Agent

This guide walks you through integrating the enhanced Scrapybara features with your existing Mama Bear system to unlock next-level capabilities.

## 🎯 What You'll Get

After following this guide, your Mama Bear will have:

- **🌐 Shared Browser Sessions** - Real-time collaboration between you and Mama Bear
- **🤖 Computer Use Agent** - Desktop automation and control
- **🔐 Authenticated Sessions** - Persistent login management
- **🔍 Multi-Instance Research** - Parallel research environments
- **🧠 Intelligent Orchestration** - Smart agent routing and collaboration
- **💾 Enhanced Memory** - Persistent context with Mem0 integration

## 📋 Prerequisites

### Required
- Python 3.9+
- Your existing Mama Bear setup
- Scrapybara API key
- Gemini API key

### Recommended  
- Anthropic API key (for Claude models)
- OpenAI API key (for GPT models)
- Mem0 API key (for enhanced memory)
- Node.js 16+ (for frontend features)

## 🚀 Quick Setup

### Step 1: Run the Enhanced Setup Script

```bash
# Download and run the setup script
python setup_enhanced_mama_bear.py
```

This will:
- ✅ Check system requirements
- ✅ Create directory structure
- ✅ Install dependencies
- ✅ Create configuration files
- ✅ Set up environment template

### Step 2: Configure API Keys

Update your `.env` file with the required API keys:

```bash
# Required for enhanced features
GEMINI_API_KEY=your_gemini_api_key_here
SCRAPYBARA_API_KEY=your_scrapybara_api_key_here

# Optional but recommended
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
MEM0_API_KEY=your_mem0_api_key_here

# Enhanced configuration
SCRAPYBARA_MAX_INSTANCES=10
SCRAPYBARA_PERMISSION_LEVEL=elevated
MAMA_BEAR_ENABLE_PROACTIVE=true
```

### Step 3: Initialize Enhanced Services

```bash
# Run the initialization script
python init_enhanced_mama_bear.py

# Start the enhanced backend
python backend/app.py
```

### Step 4: Test Enhanced Features

Open your browser and navigate to `http://localhost:5001`. You should see:

- ✅ Enhanced Mama Bear interface
- ✅ Shared browser session options
- ✅ Computer control capabilities
- ✅ Authentication management
- ✅ Research environment tools

## 🔧 Manual Integration Steps

If you prefer to integrate manually or need to customize the setup:

### 1. Add Enhanced Scrapybara Service

Create `backend/services/enhanced_scrapybara_integration.py` (provided in artifacts above)

### 2. Add Enhanced API Endpoints

Create `backend/api/enhanced_scrapybara_api.py` (provided in artifacts above)

### 3. Update Your Main App

Update your `app.py` to include enhanced initialization:

```python
# Import enhanced components
from services.enhanced_scrapybara_integration import (
    create_enhanced_scrapybara_manager,
    integrate_with_mama_bear_agents
)
from api.enhanced_scrapybara_api import integrate_enhanced_scrapybara_api

# In your initialization function
async def initialize_sanctuary_services():
    # ... existing initialization ...
    
    # Add enhanced Scrapybara
    if ENHANCED_SCRAPYBARA_AVAILABLE:
        enhanced_scrapybara_manager = await create_enhanced_scrapybara_manager(config)
        app.enhanced_scrapybara_manager = enhanced_scrapybara_manager
        
        # Integrate with Mama Bear agents
        if mama_bear_orchestrator:
            await integrate_with_mama_bear_agents(
                enhanced_scrapybara_manager, 
                mama_bear_orchestrator
            )
        
        # Add API endpoints
        integrate_enhanced_scrapybara_api(app, socketio)
```

### 4. Add Frontend Components

Add the enhanced interface component to your frontend:

```typescript
import EnhancedScrapybaraInterface from './components/enhanced/EnhancedScrapybaraInterface';

// In your main app component
<EnhancedScrapybaraInterface userId="nathan_sanctuary" />
```

## 🌐 Using Shared Browser Sessions

### Starting a Shared Session

```javascript
// Frontend JavaScript
const startSharedSession = async () => {
  const response = await fetch('/api/scrapybara/shared-browser/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      user_id: 'nathan_sanctuary',
      agent_id: 'research_specialist'
    })
  });
  
  const data = await response.json();
  console.log('Shared session started:', data.session);
};
```

### Real-time Collaboration

```javascript
// WebSocket integration
const socket = io('http://localhost:5001');

// Join shared browser session
socket.emit('join_shared_browser', {
  session_id: 'shared_abc123',
  user_id: 'nathan_sanctuary'
});

// Listen for Mama Bear suggestions
socket.on('mama_bear_suggests', (data) => {
  console.log('Mama Bear suggests:', data.suggestion);
});
```

## 🤖 Computer Use Agent Examples

### Basic Computer Control

```python
# Backend Python
from services.enhanced_scrapybara_integration import ComputerActionRequest, ComputerAction

# Take a screenshot
action_request = ComputerActionRequest(
    action_id="screenshot_001",
    action_type=ComputerAction.SCREENSHOT,
    target={},
    user_id="nathan_sanctuary"
)

result = await enhanced_scrapybara_manager.execute_computer_action(action_request)
```

### Frontend Computer Control

```javascript
// Execute computer action via API
const executeComputerAction = async (actionType, target) => {
  const response = await fetch('/api/scrapybara/computer-control/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action_type: actionType,
      target: target,
      user_id: 'nathan_sanctuary',
      permission_level: 'elevated'
    })
  });
  
  return await response.json();
};

// Examples
await executeComputerAction('screenshot', {});
await executeComputerAction('click', { selector: '.button' });
await executeComputerAction('type', { text: 'Hello World!' });
```

## 🔐 Authentication Management

### Setting Up Service Authentication

```python
# Authenticate to a service
auth_result = await enhanced_scrapybara_manager.login_to_service(
    service_name='github',
    user_id='nathan_sanctuary',
    credentials_vault_key='github_nathan_sanctuary'
)
```

### Managing Authenticated Sessions

```javascript
// Frontend - Get authenticated sessions
const getSessions = async () => {
  const response = await fetch('/api/scrapybara/auth/sessions?user_id=nathan_sanctuary');
  const data = await response.json();
  console.log('Active sessions:', data.sessions);
};
```

## 🔍 Research Environments

### Creating Research Environment

```python
# Create multi-instance research environment
research_env = await enhanced_scrapybara_manager.create_research_environment(
    research_topic='AI startups 2024',
    user_id='nathan_sanctuary'
)
```

### Parallel Research Execution

```python
# Execute multiple research queries in parallel
research_queries = [
    'AI startup funding trends 2024',
    'Machine learning infrastructure companies',
    'Generative AI market analysis'
]

results = await enhanced_scrapybara_manager.execute_collaborative_research(
    research_queries, 
    'nathan_sanctuary'
)
```

## 🧠 Intelligent Agent Orchestration

### Automatic Agent Routing

```python
# The orchestrator automatically selects the best agent
response = await mama_bear_orchestrator.process_user_request(
    message="Help me research AI companies and create a deployment plan",
    user_id="nathan_sanctuary",
    page_context="main_chat"
)

# This might route to:
# 1. Research Specialist for company research
# 2. DevOps Specialist for deployment planning
# 3. Lead Developer for coordination
```

### Agent Collaboration

```python
# Agents can communicate with each other
await mama_bear_orchestrator.send_agent_message(
    from_agent='research_specialist',
    to_agent='devops_specialist',
    message='Research complete. Ready for deployment planning.',
    context={'research_data': research_results}
)
```

## 💾 Enhanced Memory Integration

### Storing Enhanced Memories

```python
from services.mama_bear_memory_system import MemoryType, MemoryImportance

# Store collaboration memory
memory_id = await enhanced_memory.store_memory(
    content={
        'collaboration_type': 'shared_browser',
        'participants': ['user', 'research_specialist'],
        'outcome': 'successful_research',
        'findings': research_data
    },
    memory_type=MemoryType.COLLABORATION_HISTORY,
    user_id='nathan_sanctuary',
    agent_id='research_specialist',
    importance=MemoryImportance.HIGH
)
```

### Contextual Memory Retrieval

```python
# Get memories relevant to current context
relevant_memories = await enhanced_memory.get_contextual_memories(
    user_id='nathan_sanctuary',
    current_context={
        'page': 'research',
        'task_type': 'collaboration',
        'technologies': ['scrapybara', 'browser_automation']
    },
    limit=10
)
```

## 📊 Monitoring and Analytics

### System Status

```javascript
// Get comprehensive system status
const getSystemStatus = async () => {
  const response = await fetch('/api/health');
  const status = await response.json();
  console.log('System status:', status);
};
```

### Agent Performance

```javascript
// Get agent performance metrics
const getAgentStats = async () => {
  const response = await fetch('/api/mama-bear/system/stats');
  const stats = await response.json();
  console.log('Agent statistics:', stats);
};
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Enhanced Scrapybara manager not available"

**Solution:**
```bash
# Check if Scrapybara API key is set
echo $SCRAPYBARA_API_KEY

# Verify the enhanced integration is imported
grep -r "enhanced_scrapybara_integration" backend/
```

#### 2. "WebSocket connection failed"

**Solution:**
```bash
# Check if SocketIO is properly configured
# Verify CORS settings allow your frontend origin
# Check firewall/port access for WebSocket connections
```

#### 3. "Computer control actions blocked"

**Solution:**
```python
# Check permission level in request
permission_level='elevated'  # Instead of 'restricted'

# Verify safety analysis passes
# Check user permissions in system
```

#### 4. "Shared browser session not starting"

**Solution:**
```bash
# Verify Scrapybara API key and quota
curl -H "Authorization: Bearer $SCRAPYBARA_API_KEY" \
     https://api.scrapybara.com/v1/instances

# Check browser instance limits
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.getLogger('enhanced_scrapybara').setLevel(logging.DEBUG)
logging.getLogger('mama_bear_orchestration').setLevel(logging.DEBUG)
```

### Health Checks

Regular health monitoring:

```bash
# Check system health
curl http://localhost:5001/api/health

# Check agent status
curl http://localhost:5001/api/mama-bear/agents/status

# Check Scrapybara instances
curl http://localhost:5001/api/scrapybara/instances
```

## 🚀 Advanced Configurations

### Custom Agent Behaviors

```python
# Add custom computer control to agents
class CustomScoutCommander(MamaBearAgent):
    async def execute_research_workflow(self, topic):
        # Create shared browser session
        session = await self.scrapybara_manager.start_shared_browser_session(
            self.user_id, self.id
        )
        
        # Execute automated research
        workflow_result = await self.scrapybara_manager.create_computer_control_workflow(
            f"Research {topic} comprehensively using multiple sources",
            self.user_id
        )
        
        return {
            'session': session,
            'research_results': workflow_result
        }
```

### Custom Authentication Flows

```python
# Add custom service authentication
custom_auth_flow = AuthenticationFlow(
    service_name='custom_service',
    flow_steps=[
        {'action': 'navigate', 'url': 'https://custom-service.com/login'},
        {'action': 'type', 'selector': '#email', 'field': 'email'},
        {'action': 'type', 'selector': '#password', 'field': 'password'},
        {'action': 'click', 'selector': '#login-button'},
        {'action': 'wait', 'condition': 'url_contains', 'value': 'dashboard'}
    ],
    credentials_required=['email', 'password'],
    session_storage_key='custom_service_session'
)

enhanced_scrapybara_manager.auth_flows['custom_service'] = custom_auth_flow
```

## 📚 API Reference

### Enhanced Scrapybara Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrapybara/shared-browser/start` | POST | Start shared browser session |
| `/api/scrapybara/computer-control/execute` | POST | Execute computer action |
| `/api/scrapybara/auth/login` | POST | Authenticate to service |
| `/api/scrapybara/research/environment` | POST | Create research environment |
| `/api/scrapybara/research/execute` | POST | Execute collaborative research |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `join_shared_browser` | Client → Server | Join shared browser session |
| `shared_browser_action` | Client → Server | Execute shared browser action |
| `mama_bear_suggests` | Server → Client | Mama Bear suggestion |
| `computer_control_request` | Client → Server | Request computer control |
| `research_collaboration_start` | Client → Server | Start research collaboration |

## 🎉 Congratulations!

You now have a fully enhanced Mama Bear system with next-level capabilities! Your AI assistant can:

- **See and interact** with web pages alongside you
- **Control your computer** safely and intelligently  
- **Remember and learn** from your collaboration patterns
- **Orchestrate multiple agents** for complex tasks
- **Manage authenticated sessions** across services
- **Conduct parallel research** across multiple instances

## 🔗 Next Steps

1. **Explore the enhanced interface** at `http://localhost:5001`
2. **Try shared browser sessions** for collaborative web work
3. **Experiment with computer control** for automation
4. **Set up research environments** for complex projects
5. **Monitor agent collaboration** and system performance

Welcome to the future of AI-powered development assistance! 🚀✨