# backend/services/mama_bear_complete_system.py
"""
🐻 Complete Mama Bear System Integration
Brings together all components for a fully intelligent agent orchestration system
"""

import asyncio
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Import all Mama Bear components
from .mama_bear_model_manager import MamaBearModelManager
from .gemini_quota_manager import GeminiQuotaManager
from .mama_bear_orchestration import AgentOrchestrator, initialize_orchestration
from .mama_bear_workflow_logic import initialize_workflow_intelligence
from .mama_bear_memory_system import initialize_enhanced_memory
from .environment_snapshot_manager import EnvironmentSnapshotManager
from .mama_bear_observability import ProfessionalObservability
from .mama_bear_specialized_variants import *
from .mama_bear_monitoring import MamaBearMonitoring
from .ingestion_routes import bp as ingestion_bp
from .utils_routes import bp as utils_bp

# Import external dependencies
import scrapybara
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    MemoryClient = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mama_bear_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompleteMamaBearSystem:
    """
    🐻 Complete Mama Bear System
    Orchestrates all components for intelligent agent collaboration
    """
    
    def __init__(self, app: Flask, socketio: SocketIO):
        self.app = app
        self.socketio = socketio
        self.is_initialized = False
        # Register ingestion and utility routes for Mem0-powered knowledge ingestion
        self.app.register_blueprint(ingestion_bp)
        self.app.register_blueprint(utils_bp)
        
        # Core components
        self.model_manager = None
        self.memory_manager = None
        self.orchestrator = None
        self.monitoring = None
        self.scrapybara_client = None  # Will be EnhancedScrapybaraManager with hooks
        self.env_snapshot_manager = None
        self.observability = None
        
        # Specialized agents
        self.agents = {}
        
        # System state
        self.active_sessions = {}
        self.real_time_updates = True
        
    async def initialize(self):
        """Initialize all Mama Bear components"""
        try:
            logger.info("🐻 Initializing Complete Mama Bear System...")
            
            # Initialize Gemini Quota Manager
            self.gemini_quota_manager = GeminiQuotaManager()
            # Initialize Model Manager with quota failover
            self.model_manager = MamaBearModelManager(gemini_quota_manager=self.gemini_quota_manager)
            await self.model_manager.initialize()

            # Initialize Environment Snapshot Manager
            self.env_snapshot_manager = EnvironmentSnapshotManager()
            # Initialize Observability/Telemetry
            self.observability = ProfessionalObservability()
            # Initialize Enhanced Scrapybara Manager with hooks
            from .enhanced_scrapybara_manager import EnhancedScrapybaraManager
            self.scrapybara_client = EnhancedScrapybaraManager(
                env_snapshot_manager=self.env_snapshot_manager,
                observability=self.observability
            )
            
            # Initialize Memory System
            if MEM0_AVAILABLE:
                self.memory_manager = await initialize_enhanced_memory()
            else:
                logger.warning("Mem0 not available, using fallback memory")
                self.memory_manager = FallbackMemoryManager()
            
            # Initialize Scrapybara client
            try:
                self.scrapybara_client = scrapybara.Scrapybara(
                    api_key=os.getenv('SCRAPYBARA_API_KEY')
                )
            except Exception as e:
                logger.warning(f"Scrapybara initialization failed: {e}")
                self.scrapybara_client = None
            
            # Initialize Agent Orchestrator
            self.orchestrator = AgentOrchestrator(
                memory_manager=self.memory_manager,
                model_manager=self.model_manager,
                scrapybara_client=self.scrapybara_client
            )
            
            # Initialize specialized agents
            await self._initialize_specialized_agents()
            
            # Initialize monitoring
            self.monitoring = MamaBearMonitoring(
                model_manager=self.model_manager,
                orchestrator=self.orchestrator
            )
            
            # Initialize workflow intelligence
            await initialize_workflow_intelligence(self.orchestrator)
            
            # Set up real-time updates
            self._setup_real_time_updates()
            
            self.is_initialized = True
            logger.info("✅ Complete Mama Bear System initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Mama Bear System: {e}")
            raise
    
    async def _initialize_specialized_agents(self):
        """Initialize all specialized Mama Bear variants"""
        agent_configs = {
            'research_specialist': ResearchSpecialistAgent,
            'devops_specialist': DevOpsSpecialistAgent,
            'scout_commander': ScoutCommanderAgent,
            'model_coordinator': ModelCoordinatorAgent,
            'tool_curator': ToolCuratorAgent,
            'integration_architect': IntegrationArchitectAgent,
            'live_api_specialist': LiveAPISpecialistAgent
        }
        
        for agent_name, agent_class in agent_configs.items():
            try:
                agent = agent_class(
                    model_manager=self.model_manager,
                    memory_manager=self.memory_manager,
                    orchestrator=self.orchestrator
                )
                await agent.initialize()
                self.agents[agent_name] = agent
                logger.info(f"✅ Initialized {agent_name}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize {agent_name}: {e}")
    
    def _setup_real_time_updates(self):
        """Set up real-time updates via SocketIO"""
        
        @self.socketio.on('mama_bear_message')
        async def handle_message(data):
            """Handle incoming messages from clients"""
            try:
                user_id = data.get('user_id')
                message = data.get('message')
                page_context = data.get('page_context', 'main_chat')
                attachments = data.get('attachments', [])
                
                # Route to appropriate agent
                agent = self._get_agent_for_context(page_context)
                
                # Process message with full context
                response = await agent.process_message(
                    message=message,
                    user_id=user_id,
                    context={'page': page_context, 'attachments': attachments}
                )
                
                # Send response back
                emit('mama_bear_response', {
                    'response': response,
                    'agent': agent.name,
                    'timestamp': datetime.now().isoformat(),
                    'page_context': page_context
                })
                
                # Update monitoring
                await self.monitoring.log_interaction(
                    user_id=user_id,
                    agent=agent.name,
                    message=message,
                    response=response
                )
                
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                emit('mama_bear_error', {'error': str(e)})
        
        @self.socketio.on('get_system_status')
        async def handle_status_request():
            """Handle system status requests"""
            status = await self.get_system_status()
            emit('system_status', status)
        
        @self.socketio.on('create_agent_plan')
        async def handle_plan_creation(data):
            """Handle agent plan creation"""
            try:
                plan_data = data.get('plan_data')
                user_id = data.get('user_id')
                
                # Create plan through orchestrator
                plan = await self.orchestrator.create_plan(
                    title=plan_data.get('title'),
                    description=plan_data.get('description'),
                    user_id=user_id,
                    context=plan_data.get('context', {})
                )
                
                emit('agent_plan_created', {
                    'plan': plan,
                    'success': True
                })
                
            except Exception as e:
                logger.error(f"Error creating plan: {e}")
                emit('agent_plan_error', {'error': str(e)})
    
    def _get_agent_for_context(self, page_context: str):
        """Get appropriate agent for page context"""
        agent_mapping = {
            'main_chat': 'research_specialist',
            'vm_hub': 'devops_specialist', 
            'scout': 'scout_commander',
            'multi_modal': 'model_coordinator',
            'mcp_hub': 'tool_curator',
            'integration': 'integration_architect',
            'live_api': 'live_api_specialist'
        }
        
        agent_name = agent_mapping.get(page_context, 'research_specialist')
        return self.agents.get(agent_name, self.agents['research_specialist'])
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            model_status = await self.model_manager.get_status()
            memory_status = await self.memory_manager.get_status() if hasattr(self.memory_manager, 'get_status') else {'status': 'unknown'}
            
            agent_status = {}
            for name, agent in self.agents.items():
                agent_status[name] = {
                    'initialized': hasattr(agent, 'is_initialized') and agent.is_initialized,
                    'active_sessions': getattr(agent, 'active_sessions', 0),
                    'last_activity': getattr(agent, 'last_activity', None)
                }
            
            return {
                'system': {
                    'initialized': self.is_initialized,
                    'timestamp': datetime.now().isoformat()
                },
                'models': model_status,
                'memory': memory_status,
                'agents': agent_status,
                'scrapybara': {
                    'available': self.scrapybara_client is not None,
                    'status': 'connected' if self.scrapybara_client else 'disconnected'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    async def process_autonomous_task(self, task_description: str, user_id: str, context: Dict[str, Any] = None):
        """Process autonomous task through Scout Commander"""
        try:
            scout = self.agents.get('scout_commander')
            if not scout:
                raise ValueError("Scout Commander not available")
            
            result = await scout.execute_autonomous_task(
                task_description=task_description,
                user_id=user_id,
                context=context or {}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing autonomous task: {e}")
            return {'success': False, 'error': str(e)}
    
    async def create_vm_instance(self, config: Dict[str, Any], user_id: str):
        """Create VM instance through DevOps Specialist"""
        try:
            devops = self.agents.get('devops_specialist')
            if not devops:
                raise ValueError("DevOps Specialist not available")
            
            instance = await devops.create_vm_instance(config, user_id)
            return instance
            
        except Exception as e:
            logger.error(f"Error creating VM instance: {e}")
            return {'success': False, 'error': str(e)}
    
    # Example usage: snapshot VM/browser state
    async def save_environment_snapshot(self, session_id, src_path, to_cloud=False):
        if self.env_snapshot_manager:
            return self.env_snapshot_manager.save_snapshot(session_id, src_path, to_cloud=to_cloud)
        return None

    async def restore_environment_snapshot(self, session_id, archive_name, from_cloud=False):
        if self.env_snapshot_manager:
            return self.env_snapshot_manager.restore_snapshot(session_id, archive_name, from_cloud=from_cloud)
        return None

    async def shutdown(self):
        """Gracefully shutdown the system"""
        logger.info("🐻 Shutting down Complete Mama Bear System...")
        
        # Shutdown all agents
        for agent in self.agents.values():
            if hasattr(agent, 'shutdown'):
                await agent.shutdown()
        
        # Shutdown monitoring
        if self.monitoring:
            await self.monitoring.shutdown()
        
        logger.info("✅ Complete Mama Bear System shutdown complete")


class FallbackMemoryManager:
    """Fallback memory manager when Mem0 is not available"""
    
    def __init__(self):
        self.memory_store = {}
    
    async def get_context(self, user_id: str, page_context: str):
        return self.memory_store.get(f"{user_id}:{page_context}", [])
    
    async def save_interaction(self, user_id: str, message: str, response: str, context: Dict = None):
        key = f"{user_id}:{context.get('page', 'main') if context else 'main'}"
        if key not in self.memory_store:
            self.memory_store[key] = []
        
        self.memory_store[key].append({
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    async def get_status(self):
        return {
            'status': 'active',
            'type': 'fallback',
            'entries': sum(len(v) for v in self.memory_store.values())
        }


# Initialize global system
mama_bear_system = None

async def initialize_complete_system(app: Flask, socketio: SocketIO):
    """Initialize the complete Mama Bear system"""
    global mama_bear_system
    
    mama_bear_system = CompleteMamaBearSystem(app, socketio)
    await mama_bear_system.initialize()
    
    return mama_bear_system

def get_mama_bear_system():
    """Get the global Mama Bear system instance"""
    return mama_bear_system