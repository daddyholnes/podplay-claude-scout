# 🐻 Mama Bear Complete Setup & Integration Guide

Transform your existing Flask app into a sophisticated AI agent orchestration system with intelligent collaboration, persistent memory, and proactive behaviors.

## 📋 Quick Start Integration

### 1. Update Your Existing `app.py`

Replace your current app.py with this enhanced version:

```python
# app.py - Enhanced with Mama Bear Orchestration
import asyncio
import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

# Your existing imports
from taskmaster_ai import init_app as init_taskmaster_ai
from mama_bear_config_setup import load_config

# New Mama Bear imports
from mama_bear_complete_system import create_mama_bear_app, CompleteMamaBearSystem

async def create_enhanced_app():
    """Create Flask app with full Mama Bear intelligence"""
    
    print("🐻 Initializing Mama Bear Development Sanctuary...")
    
    # Load configuration
    config = load_config()
    
    # Create the complete Mama Bear system
    app = await create_mama_bear_app(config)
    
    # Initialize your existing components
    init_taskmaster_ai(app)
    
    # Add any additional integrations
    try:
        from mem0_integration import persist_to_mem0
        app.persist_to_mem0 = persist_to_mem0
    except ImportError:
        print("[INFO] Mem0 integration using enhanced system")
    
    try:
        from scrapybara_integration import bp as scrapybara_bp
        app.register_blueprint(scrapybara_bp, url_prefix='/api')
    except ImportError:
        print("[INFO] Scrapybara integration using enhanced system")
    
    print("🎉 Mama Bear Sanctuary is ready!")
    return app

def run_app():
    """Run the enhanced application"""
    
    # Create and run the app
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        app = loop.run_until_complete(create_enhanced_app())
        
        # Get the Mama Bear system for running
        system = app.mama_bear_system
        system.run(host="0.0.0.0", port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("👋 Mama Bear says goodbye!")
    finally:
        loop.close()

if __name__ == "__main__":
    run_app()
```

### 2. Update Your Environment Variables

Add these to your `.env` file:

```bash
# Enhanced Mama Bear Configuration
GEMINI_API_KEY=AIzaSyCNUGhuoAvvaSJ2ypsqzgtUCaLSusRZs5Y
GEMINI_API_KEY_BACKUP=your_second_gemini_key_here  # Optional but recommended

# Existing APIs
ANTHROPIC_API_KEY=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
OPENAI_API_KEY=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

# Scrapybara
SCRAPYBARA_API_KEY=scrapy-abaf2356-01d5-4d65-88d3-eebcd177b214

# Mem0.ai
MEM0_API_KEY=m0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg
MEM0_USER_ID=nathan_sanctuary

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/home/woody/Podplay-Sanctuary/podplay-build-beta-10490f7d079e.json
GOOGLE_CLOUD_PROJECT=podplay-build-beta

# Enhanced System Configuration
MAMA_BEAR_ENABLE_PROACTIVE=true
MAMA_BEAR_DAILY_BRIEFING=true
MAMA_BEAR_AUTO_OPTIMIZE=true
MAMA_BEAR_MEMORY_RETENTION_DAYS=30
```

### 3. Install Additional Dependencies

```bash
pip install asyncio aiofiles python-socketio
pip install mem0ai  # Optional but recommended
pip install scrapybara  # If not already installed
```

## 🏗️ File Structure

Your project should now have this structure:

```
your-project/
├── app.py (updated)
├── mama_bear_config_setup.py (existing)
├── init_db.py (existing)
├── backend/
│   ├── services/
│   │   ├── mama_bear_model_manager.py (new)
│   │   ├── mama_bear_orchestration.py (new)
│   │   ├── mama_bear_workflow_logic.py (new)
│   │   ├── mama_bear_memory_system.py (new)
│   │   └── mama_bear_specialized_variants.py (existing)
│   ├── api/
│   │   └── mama_bear_orchestration_api.py (new)
│   ├── utils/
│   │   └── mama_bear_monitoring.py (existing)
│   └── mama_bear_complete_system.py (new)
├── frontend/
│   └── src/
│       └── components/
│           └── orchestration/
│               └── MamaBearOrchestration.tsx (new)
└── mama_bear_memory/ (created automatically)
    ├── memories/
    ├── profiles/
    └── patterns/
```

## 🎭 Agent Types & Capabilities

Your Mama Bear system now includes these specialized agents:

### 1. **Research Specialist** 🔍
- **Purpose**: Deep research, web search, document analysis
- **Tools**: Scrapybara browser automation, RAG retrieval, web search
- **Best For**: Complex research tasks, information gathering, analysis

### 2. **DevOps Specialist** ⚙️
- **Purpose**: Infrastructure, deployment, optimization
- **Tools**: VM management, container orchestration, monitoring
- **Best For**: Deployment tasks, performance tuning, system management

### 3. **Scout Commander** 🧭
- **Purpose**: Autonomous exploration and task execution
- **Tools**: Scrapybara desktop control, file system access, long-running tasks
- **Best For**: Autonomous workflows, data collection, exploration tasks

### 4. **Model Coordinator** 🤖
- **Purpose**: AI model management and optimization
- **Tools**: Model selection, fine-tuning, performance monitoring
- **Best For**: Model-related tasks, AI optimization, cross-model synthesis

### 5. **Tool Curator** 🛠️
- **Purpose**: Tool discovery and integration
- **Tools**: MCP marketplace, GitHub search, compatibility checking
- **Best For**: Finding new tools, integration recommendations

### 6. **Integration Architect** 🔗
- **Purpose**: API connections and system integration
- **Tools**: API testing, authentication setup, workflow automation
- **Best For**: Building integrations, API work, system connections

### 7. **Live API Specialist** ⚡
- **Purpose**: Real-time features and live interactions
- **Tools**: WebSocket management, streaming APIs, live data processing
- **Best For**: Real-time features, live demos, interactive experiences

### 8. **Lead Developer** 👨‍💻
- **Purpose**: Planning, coordination, complex development
- **Tools**: All tools available, agent coordination, project planning
- **Best For**: Complex projects, team coordination, architecture decisions

## 🔄 Workflow Types

The system automatically detects and routes these workflow types:

1. **Simple Query** - Quick questions → Single agent
2. **Research Task** - Deep analysis → Research + Scout collaboration
3. **Code Generation** - Development work → Lead Developer + specialists
4. **Deployment Task** - Infrastructure work → DevOps + Integration
5. **Complex Project** - Multi-step projects → Full team collaboration
6. **Troubleshooting** - Problem solving → Diagnostic team
7. **Learning Session** - Educational content → Research + Tool Curator

## 🚀 Usage Examples

### Frontend Integration

```typescript
// In your React components
import { MamaBearOrchestrationInterface } from './components/orchestration/MamaBearOrchestration';

function App() {
  return (
    <MamaBearOrchestrationInterface 
      userId="nathan_sanctuary"
      pageContext="main_chat"
      view="chat"
    />
  );
}
```

### API Usage

```javascript
// Simple chat with intelligent routing
const response = await fetch('/api/mama-bear/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Help me build a real-time chat app with WebSockets",
    user_id: "nathan_sanctuary",
    page_context: "main_chat"
  })
});

// Direct agent communication
const directResponse = await fetch('/api/mama-bear/agents/lead_developer/direct', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Review this code architecture",
    user_id: "nathan_sanctuary"
  })
});

// Get system status
const status = await fetch('/api/mama-bear/agents/status');
const statusData = await status.json();
```

### WebSocket Real-time Communication

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

// Join orchestration room
socket.emit('join_orchestration', { user_id: 'nathan_sanctuary' });

// Send message with real-time routing
socket.emit('mama_bear_chat_realtime', {
  message: "Deploy my app to production",
  user_id: "nathan_sanctuary", 
  page_context: "vm_hub"
});

// Listen for responses
socket.on('mama_bear_response', (data) => {
  console.log('Mama Bear response:', data);
});

// Listen for system updates
socket.on('system_status_update', (status) => {
  console.log('System status:', status);
});
```

## 🧠 How Mama Bear Knows What She's Doing

### 1. **Context Awareness System**
- Tracks conversation history and user patterns
- Maintains project context and current focus
- Learns from user expertise level and preferences
- Preserves context across page navigation and sessions

### 2. **Intelligent Decision Engine**
- Analyzes message complexity and intent
- Considers user history and success patterns
- Selects optimal agents based on capabilities
- Estimates resource requirements and duration

### 3. **Workflow Intelligence**
- Pattern recognition from historical interactions
- Success correlation analysis
- Automatic workflow optimization
- Fallback strategies for failures

### 4. **Memory & Learning System**
- Persistent conversation memory with Mem0 integration
- User profile building and preference learning
- Agent performance tracking and optimization
- Pattern analysis for continuous improvement

### 5. **Proactive Behaviors**
- Daily briefings with system updates
- Automatic quota management and failover
- Performance monitoring and optimization
- Health checks and self-recovery

## 📊 Monitoring & Analytics

### Built-in Dashboards

Access comprehensive monitoring at:
- `/health` - System health check
- WebSocket events for real-time updates
- Built-in performance analytics
- Agent collaboration metrics

### Key Metrics Tracked

- **Agent Performance**: Success rates, response times, user satisfaction
- **Model Usage**: API quota, billing distribution, error rates
- **Collaboration**: Team effectiveness, workflow optimization
- **User Patterns**: Learning progression, preference evolution

## 🔧 Advanced Configuration

### Custom Agent Behaviors

```python
# Add custom agent behavior
from services.mama_bear_specialized_variants import MamaBearVariant

class CustomSpecialist(MamaBearVariant):
    def get_system_prompt(self):
        return "Your custom agent personality and capabilities"
    
    def get_model_preferences(self):
        return {
            'prefers_pro_model': True,
            'temperature': 0.5,
            'requires_reasoning': True
        }

# Register with orchestrator
orchestrator.agents['custom_specialist'] = MamaBearAgent('custom_specialist', CustomSpecialist(), orchestrator)
```

### Workflow Customization

```python
# Add custom workflow template
orchestrator.workflow_intelligence.workflow_templates['custom_workflow'] = {
    "agent_sequence": ["custom_specialist", "lead_developer"],
    "collaboration_type": "collaborative",
    "max_duration": 60,
    "tools_required": ["custom_tool"],
    "success_metrics": ["custom_metric"]
}
```

## 🚨 Troubleshooting

### Common Issues

1. **"Agent not responding"**
   - Check model API quotas in logs
   - Verify network connectivity
   - System will auto-fallback to backup models

2. **"Memory system errors"**
   - Ensure write permissions for `mama_bear_memory/` directory
   - Check disk space availability
   - Mem0 integration is optional - local storage is fallback

3. **"Orchestration failures"**
   - Check that all agents are properly initialized
   - Verify configuration in `mama_bear_config_setup.py`
   - System includes automatic recovery mechanisms

### Debug Mode

```python
# Enable detailed logging
import logging
logging.getLogger('mama_bear').setLevel(logging.DEBUG)

# Or start with debug flag
system.run(debug=True)
```

## 🎯 Next Steps

1. **Test the System**: Start with simple queries to verify everything works
2. **Customize Agents**: Add your specific domain knowledge to agent prompts
3. **Monitor Performance**: Use the built-in dashboards to optimize
4. **Extend Capabilities**: Add new tools and integrations as needed
5. **Scale Up**: The system is designed to handle complex, long-running workflows

## 💡 Pro Tips

- **Start Simple**: Begin with basic chat interactions before complex workflows
- **Monitor Quotas**: Keep an eye on API usage across all models
- **User Feedback**: The system learns from user satisfaction ratings
- **Regular Updates**: Keep your agent configurations updated as needs evolve
- **Backup Keys**: Always configure backup API keys for reliability

---

🐻 **Your Mama Bear is now fully equipped to handle complex, collaborative AI workflows with intelligence, persistence, and care. Welcome to your AI Development Sanctuary!** 🚀✨