# backend/mama_bear_complete_system.py
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
from services.mama_bear_model_manager import MamaBearModelManager
from services.mama_bear_orchestration import AgentOrchestrator, initialize_orchestration
from services.mama_bear_workflow_logic import initialize_workflow_intelligence
from services.mama_bear_memory_system import initialize_enhanced_memory
from services.mama_bear_specialized_variants import *
from api.mama_bear_orchestration_api import integrate_orchestration_with_app
from utils.mama_bear_monitoring import MamaBearMonitoring
from config.mama_bear_config_setup import load_config

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
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or load_config()
        self.app = None
        self.socketio = None
        
        # Core components
        self.model_manager = None
        self.memory_manager = None
        self.orchestrator = None
        self.workflow_intelligence = None
        self.monitoring = None
        self.scrapybara_client = None
        
        # External services
        self.mem0_client = None
        
        # System state
        self.is_initialized = False
        self.startup_time = None
        
    async def initialize(self) -> Flask:
        """Initialize the complete Mama Bear system"""
        
        logger.info("🐻 Starting Mama Bear System initialization...")
        start_time = datetime.now()
        
        try:
            # 1. Initialize external services
            await self._initialize_external_services()
            
            # 2. Initialize core AI components
            await self._initialize_ai_components()
            
            # 3. Initialize Flask application
            self._initialize_flask_app()
            
            # 4. Initialize orchestration system
            await self._initialize_orchestration()
            
            # 5. Initialize monitoring and analytics
            await self._initialize_monitoring()
            
            # 6. Start background services
            await self._start_background_services()
            
            # 7. Perform system health check
            await self._perform_health_check()
            
            self.is_initialized = True
            self.startup_time = datetime.now()
            
            initialization_time = (self.startup_time - start_time).total_seconds()
            logger.info(f"🎉 Mama Bear System initialized successfully in {initialization_time:.2f} seconds!")
            
            # Send startup notification
            await self._send_startup_notification()
            
            return self.app
            
        except Exception as e:
            logger.error(f"❌ Mama Bear System initialization failed: {e}")
            raise
    
    async def _initialize_external_services(self):
        """Initialize external services"""
        
        logger.info("🔌 Initializing external services...")
        
        # Initialize Scrapybara
        try:
            api_key = self.config.get('SCRAPYBARA_API_KEY')
            if api_key:
                self.scrapybara_client = scrapybara.Scrapybara(api_key=api_key)
                logger.info("✅ Scrapybara initialized")
            else:
                logger.warning("⚠️ Scrapybara API key not found")
        except Exception as e:
            logger.warning(f"⚠️ Scrapybara initialization failed: {e}")
        
        # Initialize Mem0
        if MEM0_AVAILABLE:
            try:
                mem0_api_key = self.config.get('MEM0_API_KEY')
                if mem0_api_key:
                    self.mem0_client = MemoryClient(api_key=mem0_api_key)
                    logger.info("✅ Mem0 initialized")
                else:
                    logger.warning("⚠️ Mem0 API key not found")
            except Exception as e:
                logger.warning(f"⚠️ Mem0 initialization failed: {e}")
        else:
            logger.warning("⚠️ Mem0 not available - install mem0ai package")
    
    async def _initialize_ai_components(self):
        """Initialize core AI components"""
        
        logger.info("🤖 Initializing AI components...")
        
        # Initialize model manager with intelligent quota management
        self.model_manager = MamaBearModelManager()
        await self.model_manager.warm_up_models()
        logger.info("✅ Model Manager initialized")
        
        # Initialize enhanced memory system
        self.memory_manager = initialize_enhanced_memory(self.mem0_client)
        logger.info("✅ Memory Manager initialized")
        
        # Initialize workflow intelligence
        self.workflow_intelligence, self.collaboration_orchestrator = initialize_workflow_intelligence(
            self.model_manager, 
            self.memory_manager
        )
        logger.info("✅ Workflow Intelligence initialized")
    
    def _initialize_flask_app(self):
        """Initialize Flask application"""
        
        logger.info("🌐 Initializing Flask application...")
        
        self.app = Flask(__name__)
        self.app.config.update(self.config)
        
        # Initialize extensions
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Register health check endpoint
        @self.app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy' if self.is_initialized else 'initializing',
                'startup_time': self.startup_time.isoformat() if self.startup_time else None,
                'components': {
                    'model_manager': self.model_manager is not None,
                    'memory_manager': self.memory_manager is not None,
                    'orchestrator': self.orchestrator is not None,
                    'scrapybara': self.scrapybara_client is not None,
                    'mem0': self.mem0_client is not None
                }
            })
        
        # Store components in app context
        self.app.mama_bear_model_manager = self.model_manager
        self.app.mama_bear_memory_manager = self.memory_manager
        self.app.mama_bear_scrapybara_client = self.scrapybara_client
        
        logger.info("✅ Flask application initialized")
    
    async def _initialize_orchestration(self):
        """Initialize agent orchestration system"""
        
        logger.info("🎭 Initializing orchestration system...")
        
        # Initialize orchestrator with all components
        self.orchestrator = await initialize_orchestration(
            self.app,
            self.memory_manager,
            self.model_manager,
            self.scrapybara_client
        )
        
        # Integrate workflow intelligence
        self.orchestrator.workflow_intelligence = self.workflow_intelligence
        self.orchestrator.collaboration_orchestrator = self.collaboration_orchestrator
        
        # Integrate API endpoints and WebSocket handlers
        integrate_orchestration_with_app(
            self.app,
            self.socketio,
            self.memory_manager,
            self.model_manager,
            self.scrapybara_client
        )
        
        logger.info("✅ Orchestration system initialized")
    
    async def _initialize_monitoring(self):
        """Initialize monitoring and analytics"""
        
        logger.info("📊 Initializing monitoring...")
        
        self.monitoring = MamaBearMonitoring(self.model_manager)
        self.app.mama_bear_monitoring = self.monitoring
        
        logger.info("✅ Monitoring initialized")
    
    async def _start_background_services(self):
        """Start background services"""
        
        logger.info("⚙️ Starting background services...")
        
        # Start system monitoring
        asyncio.create_task(self._system_health_monitor())
        
        # Start proactive agent behaviors
        asyncio.create_task(self._proactive_agent_loop())
        
        # Start performance optimization
        asyncio.create_task(self._performance_optimization_loop())
        
        logger.info("✅ Background services started")
    
    async def _perform_health_check(self):
        """Perform comprehensive system health check"""
        
        logger.info("🏥 Performing system health check...")
        
        health_results = {}
        
        # Check model manager
        try:
            model_status = self.model_manager.get_model_status()
            healthy_models = sum(1 for m in model_status['models'] if m['status'] != 'error')
            total_models = len(model_status['models'])
            health_results['model_manager'] = {
                'status': 'healthy' if healthy_models > 0 else 'degraded',
                'healthy_models': f"{healthy_models}/{total_models}"
            }
        except Exception as e:
            health_results['model_manager'] = {'status': 'error', 'error': str(e)}
        
        # Check memory manager
        try:
            # Test memory operations
            test_memory = await self.memory_manager.save_interaction(
                user_id='health_check',
                message='System health check',
                response='Health check successful',
                metadata={'test': True}
            )
            health_results['memory_manager'] = {'status': 'healthy'}
        except Exception as e:
            health_results['memory_manager'] = {'status': 'error', 'error': str(e)}
        
        # Check orchestrator
        try:
            orchestrator_status = await self.orchestrator.get_system_status()
            active_agents = sum(1 for agent in orchestrator_status['agents'].values() 
                              if agent['state'] != 'error')
            total_agents = len(orchestrator_status['agents'])
            health_results['orchestrator'] = {
                'status': 'healthy' if active_agents == total_agents else 'degraded',
                'active_agents': f"{active_agents}/{total_agents}"
            }
        except Exception as e:
            health_results['orchestrator'] = {'status': 'error', 'error': str(e)}
        
        # Check external services
        if self.scrapybara_client:
            health_results['scrapybara'] = {'status': 'available'}
        else:
            health_results['scrapybara'] = {'status': 'unavailable'}
        
        if self.mem0_client:
            health_results['mem0'] = {'status': 'available'}
        else:
            health_results['mem0'] = {'status': 'unavailable'}
        
        # Overall health assessment
        critical_components = ['model_manager', 'memory_manager', 'orchestrator']
        healthy_critical = sum(1 for comp in critical_components 
                             if health_results.get(comp, {}).get('status') == 'healthy')
        
        overall_status = 'healthy' if healthy_critical == len(critical_components) else 'degraded'
        
        logger.info(f"🏥 Health check complete - Overall status: {overall_status}")
        for component, status in health_results.items():
            logger.info(f"  {component}: {status}")
        
        return health_results
    
    async def _send_startup_notification(self):
        """Send startup notification to connected clients"""
        
        if self.socketio:
            self.socketio.emit('mama_bear_system_ready', {
                'message': '🐻 Mama Bear is ready to help!',
                'startup_time': self.startup_time.isoformat(),
                'capabilities': [
                    'Intelligent model selection',
                    'Multi-agent collaboration',
                    'Persistent memory',
                    'Scrapybara integration',
                    'Proactive assistance'
                ]
            })
    
    async def _system_health_monitor(self):
        """Background task to monitor system health"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Perform health checks
                health_results = await self._perform_health_check()
                
                # Alert on critical issues
                critical_issues = [
                    comp for comp, status in health_results.items()
                    if status.get('status') == 'error'
                ]
                
                if critical_issues:
                    logger.warning(f"🚨 Critical health issues detected: {critical_issues}")
                    
                    # Attempt automatic recovery
                    for component in critical_issues:
                        await self._attempt_component_recovery(component)
                
                # Broadcast health update
                if self.socketio:
                    self.socketio.emit('system_health_update', {
                        'timestamp': datetime.now().isoformat(),
                        'health_results': health_results
                    })
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _attempt_component_recovery(self, component: str):
        """Attempt to recover a failed component"""
        
        logger.info(f"🔧 Attempting recovery for component: {component}")
        
        try:
            if component == 'model_manager':
                # Reinitialize model manager
                self.model_manager = MamaBearModelManager()
                await self.model_manager.warm_up_models()
                
            elif component == 'memory_manager':
                # Reinitialize memory manager
                self.memory_manager = initialize_enhanced_memory(self.mem0_client)
                
            elif component == 'orchestrator':
                # Reinitialize orchestrator
                self.orchestrator = await initialize_orchestration(
                    self.app,
                    self.memory_manager,
                    self.model_manager,
                    self.scrapybara_client
                )
            
            logger.info(f"✅ Component recovery successful: {component}")
            
        except Exception as e:
            logger.error(f"❌ Component recovery failed for {component}: {e}")
    
    async def _proactive_agent_loop(self):
        """Proactive agent behaviors"""
        
        while True:
            try:
                await asyncio.sleep(1800)  # Every 30 minutes
                
                # Daily briefing at 9 AM
                current_hour = datetime.now().hour
                if current_hour == 9:
                    await self._send_daily_briefing()
                
                # Check for system optimizations
                await self._check_system_optimizations()
                
                # Update user profiles
                await self._update_user_profiles()
                
            except Exception as e:
                logger.error(f"Proactive agent loop error: {e}")
                await asyncio.sleep(300)
    
    async def _send_daily_briefing(self):
        """Send daily briefing to active users"""
        
        logger.info("📋 Preparing daily briefing...")
        
        # Get system statistics
        if self.monitoring:
            daily_report = self.monitoring.generate_daily_report()
            
            briefing_message = f"""
            🐻 Good morning! Here's your daily Mama Bear briefing:
            
            📊 **System Health**: {daily_report['summary']['success_rate']:.1f}% success rate
            🚀 **Performance**: {daily_report['summary']['average_response_time']:.2f}s avg response
            🤖 **AI Models**: {len(daily_report['model_performance'])} models available
            
            💡 **Recommendations**:
            {chr(10).join(f"• {rec}" for rec in daily_report['recommendations'][:3])}
            
            Ready to help you build amazing things today! 🚀
            """
            
            # Broadcast to all connected clients
            if self.socketio:
                self.socketio.emit('daily_briefing', {
                    'message': briefing_message,
                    'timestamp': datetime.now().isoformat(),
                    'report': daily_report
                })
    
    async def _check_system_optimizations(self):
        """Check for possible system optimizations"""
        
        # Model performance optimization
        if self.model_manager:
            model_status = self.model_manager.get_model_status()
            
            # Check for consistently failing models
            failing_models = [
                model for model in model_status['models']
                if model.get('error_count', 0) > 10
            ]
            
            if failing_models:
                logger.info(f"🔧 Found models needing attention: {[m['name'] for m in failing_models]}")
                # Could implement automatic model rotation or cooldown here
        
        # Memory optimization
        if self.memory_manager:
            # The memory manager handles its own consolidation
            pass
    
    async def _update_user_profiles(self):
        """Update user profiles based on recent interactions"""
        
        # This would analyze recent interactions and update user preferences
        # The memory manager handles most of this automatically
        pass
    
    async def _performance_optimization_loop(self):
        """Performance optimization background task"""
        
        while True:
            try:
                await asyncio.sleep(3600)  # Every hour
                
                # Optimize memory usage
                await self._optimize_memory_usage()
                
                # Optimize model selection
                await self._optimize_model_selection()
                
                # Clean up temporary data
                await self._cleanup_temporary_data()
                
            except Exception as e:
                logger.error(f"Performance optimization error: {e}")
                await asyncio.sleep(300)
    
    async def _optimize_memory_usage(self):
        """Optimize memory usage"""
        
        # Clear old cached data
        if hasattr(self.orchestrator, 'context_awareness'):
            context = self.orchestrator.context_awareness
            
            # Remove old global context entries
            cutoff = datetime.now() - timedelta(hours=24)
            old_keys = [
                key for key, data in context.global_context.items()
                if data.get('timestamp', datetime.now()) < cutoff
            ]
            
            for key in old_keys:
                del context.global_context[key]
            
            if old_keys:
                logger.info(f"🧹 Cleaned up {len(old_keys)} old context entries")
    
    async def _optimize_model_selection(self):
        """Optimize model selection based on performance"""
        
        # Analyze model performance and adjust priorities
        if self.monitoring:
            daily_report = self.monitoring.generate_daily_report()
            model_performance = daily_report.get('model_performance', {})
            
            # Identify best performing models
            best_models = sorted(
                model_performance.items(),
                key=lambda x: x[1].get('usage_percentage', 0),
                reverse=True
            )[:3]
            
            if best_models:
                logger.info(f"🏆 Top performing models: {[m[0] for m in best_models]}")
    
    async def _cleanup_temporary_data(self):
        """Clean up temporary data"""
        
        # Clean up old collaboration sessions
        if hasattr(self.orchestrator, 'collaboration_sessions'):
            cutoff = datetime.now() - timedelta(hours=6)
            old_sessions = [
                session_id for session_id, session in self.orchestrator.collaboration_sessions.items()
                if session.get('started_at', datetime.now()) < cutoff
            ]
            
            for session_id in old_sessions:
                del self.orchestrator.collaboration_sessions[session_id]
            
            if old_sessions:
                logger.info(f"🧹 Cleaned up {len(old_sessions)} old collaboration sessions")
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the complete Mama Bear system"""
        
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        logger.info(f"🚀 Starting Mama Bear System on {host}:{port}")
        
        self.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug,
            allow_unsafe_werkzeug=True
        )

# Convenience function for easy setup
async def create_mama_bear_app(config: Dict[str, Any] = None) -> Flask:
    """
    Create and initialize a complete Mama Bear application
    
    Usage:
        app = await create_mama_bear_app()
        # or with custom config:
        app = await create_mama_bear_app({'CUSTOM_SETTING': 'value'})
    """
    
    system = CompleteMamaBearSystem(config)
    app = await system.initialize()
    
    # Store system reference in app for access
    app.mama_bear_system = system
    
    return app

# Main entry point
async def main():
    """Main entry point for running the complete system"""
    
    logger.info("🐻 Welcome to Mama Bear - Your AI Development Sanctuary")
    
    try:
        # Create and initialize the system
        system = CompleteMamaBearSystem()
        app = await system.initialize()
        
        # Run the system
        system.run(debug=True)
        
    except KeyboardInterrupt:
        logger.info("👋 Mama Bear says goodbye!")
    except Exception as e:
        logger.error(f"💥 System error: {e}")
        raise

if __name__ == "__main__":
    # Set up event loop for async main
    asyncio.run(main())