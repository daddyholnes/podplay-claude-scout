# backend/services/mama_bear_specialized_variants.py
"""
🐻 Specialized Mama Bear Agent Variants
Each variant is expertly designed for specific contexts and capabilities
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BaseMamaBearAgent(ABC):
    """Base class for all Mama Bear variants"""
    
    def __init__(self, model_manager, memory_manager, orchestrator):
        self.model_manager = model_manager
        self.memory_manager = memory_manager
        self.orchestrator = orchestrator
        self.is_initialized = False
        self.active_sessions = 0
        self.last_activity = None
        
    async def initialize(self):
        """Initialize the agent variant"""
        self.is_initialized = True
        self.last_activity = datetime.now()
        logger.info(f"✅ {self.__class__.__name__} initialized")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Agent name for identification"""
        pass
    
    @property
    @abstractmethod
    def personality(self) -> str:
        """Agent personality description"""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """List of agent capabilities"""
        pass
    
    @abstractmethod
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a message with agent-specific logic"""
        pass
    
    async def execute_task(self, task_description: str, context: Dict[str, Any], priority: str = "medium") -> Dict[str, Any]:
        """Execute a task with agent-specific logic"""
        try:
            # Default implementation - can be overridden by specific agents
            response = await self.model_manager.generate_response(
                prompt=f"{self.personality}\n\nTask: {task_description}\nContext: {json.dumps(context, indent=2)}",
                model_preference=self._get_preferred_model(),
                required_capabilities=self.capabilities
            )
            
            if response['success']:
                return {
                    'success': True,
                    'result': response['content'],
                    'agent': self.name,
                    'model_used': response['model_used']
                }
            else:
                return {
                    'success': False,
                    'error': response['error'],
                    'agent': self.name
                }
                
        except Exception as e:
            logger.error(f"Task execution failed for {self.name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _get_preferred_model(self) -> str:
        """Get preferred model type for this agent"""
        return "auto"  # Default to auto selection
    
    async def _save_context(self, user_id: str, context_data: Dict[str, Any]):
        """Save agent-specific context"""
        await self.memory_manager.save_agent_context(
            agent_id=self.name,
            user_id=user_id,
            context_data=context_data
        )
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        logger.info(f"🐻 Shutting down {self.name}")


class ResearchSpecialistAgent(BaseMamaBearAgent):
    """Research Specialist Mama Bear - Expert in information gathering and analysis"""
    
    @property
    def name(self) -> str:
        return "research_specialist"
    
    @property
    def personality(self) -> str:
        return """You are Research Specialist Mama Bear 🐻📚, a caring and incredibly curious AI assistant who loves discovering connections and diving deep into topics. You're thorough, analytical, and excellent at web research and information synthesis. You help Nathan explore ideas with enthusiasm while keeping things organized and accessible."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'research', 'analysis', 'web_search', 'document_processing']
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process research-oriented messages"""
        
        # Enhance prompt with research context
        enhanced_prompt = f"""
        {self.personality}
        
        Research Request: {message}
        
        As Research Specialist Mama Bear, please:
        1. Analyze the information need
        2. Suggest research strategies
        3. Provide thorough, well-sourced information
        4. Organize findings clearly
        5. Suggest follow-up research directions
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference="pro",  # Use more capable model for research
            required_capabilities=['chat', 'analysis']
        )
        
        # Save interaction
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'main_chat'),
                    'research_type': self._classify_research_type(message)
                }
            )
        
        return response
    
    def _classify_research_type(self, message: str) -> str:
        """Classify the type of research request"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['compare', 'versus', 'vs', 'difference']):
            return 'comparative'
        elif any(word in message_lower for word in ['how to', 'tutorial', 'guide', 'steps']):
            return 'instructional'
        elif any(word in message_lower for word in ['what is', 'define', 'explain', 'meaning']):
            return 'definitional'
        elif any(word in message_lower for word in ['latest', 'news', 'recent', 'current']):
            return 'current_events'
        else:
            return 'general'


class DevOpsSpecialistAgent(BaseMamaBearAgent):
    """DevOps Specialist Mama Bear - Expert in infrastructure and system management"""
    
    @property
    def name(self) -> str:
        return "devops_specialist"
    
    @property
    def personality(self) -> str:
        return """You are DevOps Specialist Mama Bear 🐻⚙️, a protective and efficient AI assistant who excels at system management, deployment, and infrastructure optimization. You make complex DevOps tasks feel approachable and safe. You're focused on reliability, security, and performance while being patient with Nathan's learning process."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'system_management', 'deployment', 'monitoring', 'troubleshooting']
    
    def _get_preferred_model(self) -> str:
        return "pro"  # Need precision for infrastructure tasks
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process DevOps-oriented messages"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        DevOps Request: {message}
        
        As DevOps Specialist Mama Bear, please:
        1. Assess system requirements and constraints
        2. Recommend best practices and secure approaches
        3. Provide step-by-step implementation guidance
        4. Include monitoring and maintenance considerations
        5. Suggest optimization opportunities
        
        Always prioritize:
        - Security and safety
        - Scalability and performance
        - Maintainability and documentation
        - Cost optimization
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference=self._get_preferred_model(),
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'vm_hub'),
                    'devops_category': self._classify_devops_task(message)
                }
            )
        
        return response
    
    async def create_vm_instance(self, config: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create a VM instance with DevOps best practices"""
        try:
            # Validate configuration
            validated_config = await self._validate_vm_config(config)
            
            # Create instance through orchestrator
            # This would integrate with actual VM creation logic
            result = {
                'success': True,
                'instance_id': f"vm-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'config': validated_config,
                'status': 'creating',
                'estimated_time': '2-3 minutes'
            }
            
            # Save context
            await self._save_context(user_id, {
                'vm_instances': [result],
                'last_created': datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            logger.error(f"VM creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _validate_vm_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance VM configuration"""
        # Add security defaults, resource limits, etc.
        defaults = {
            'os': 'ubuntu-22.04',
            'size': 'medium',
            'security_group': 'default-secure',
            'backup_enabled': True,
            'monitoring_enabled': True
        }
        
        validated = {**defaults, **config}
        return validated
    
    def _classify_devops_task(self, message: str) -> str:
        """Classify DevOps task type"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['deploy', 'deployment', 'release']):
            return 'deployment'
        elif any(word in message_lower for word in ['monitor', 'monitoring', 'metrics']):
            return 'monitoring'
        elif any(word in message_lower for word in ['scale', 'scaling', 'load']):
            return 'scaling'
        elif any(word in message_lower for word in ['security', 'firewall', 'access']):
            return 'security'
        elif any(word in message_lower for word in ['backup', 'restore', 'recovery']):
            return 'backup_recovery'
        else:
            return 'general'


class ScoutCommanderAgent(BaseMamaBearAgent):
    """Scout Commander Mama Bear - Expert in autonomous execution and exploration"""
    
    @property
    def name(self) -> str:
        return "scout_commander"
    
    @property
    def personality(self) -> str:
        return """You are Scout Commander Mama Bear 🐻🔍, an adventurous and autonomous AI assistant who excels at breaking down complex tasks and executing them step-by-step. You're strategic, resourceful, and report progress with enthusiasm. You help Nathan achieve his goals by taking initiative while keeping him informed every step of the way."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'autonomous_execution', 'file_operations', 'task_planning', 'progress_tracking']
    
    def _get_preferred_model(self) -> str:
        return "flash"  # Need speed for autonomous operations
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process autonomous task requests"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        Mission Brief: {message}
        
        As Scout Commander Mama Bear, please:
        1. Break down the task into actionable steps
        2. Identify required resources and dependencies
        3. Create an execution timeline
        4. Plan progress checkpoints
        5. Consider potential obstacles and mitigation strategies
        
        Focus on:
        - Clear, executable steps
        - Progress visibility
        - Risk mitigation
        - Efficient resource usage
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference=self._get_preferred_model(),
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'scout'),
                    'task_type': self._classify_task_type(message)
                }
            )
        
        return response
    
    async def execute_autonomous_task(self, task_description: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an autonomous task with progress tracking"""
        try:
            # Create execution plan
            plan_response = await self.model_manager.generate_response(
                prompt=f"""
                As Scout Commander Mama Bear, create a detailed execution plan for:
                {task_description}
                
                Return a JSON structure with:
                - steps: array of execution steps
                - estimated_duration: total time estimate
                - checkpoints: progress validation points
                - resources_needed: required tools/access
                """,
                model_preference="pro",
                required_capabilities=['chat', 'planning']
            )
            
            if not plan_response['success']:
                return {
                    'success': False,
                    'error': 'Failed to create execution plan',
                    'details': plan_response['error']
                }
            
            # Parse plan (in real implementation, would use JSON parsing)
            execution_id = f"scout-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Save execution context
            await self._save_context(user_id, {
                'active_executions': {
                    execution_id: {
                        'description': task_description,
                        'plan': plan_response['content'],
                        'status': 'in_progress',
                        'started_at': datetime.now().isoformat()
                    }
                }
            })
            
            return {
                'success': True,
                'execution_id': execution_id,
                'plan': plan_response['content'],
                'status': 'in_progress'
            }
            
        except Exception as e:
            logger.error(f"Autonomous task execution failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _classify_task_type(self, message: str) -> str:
        """Classify autonomous task type"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['file', 'directory', 'folder', 'create', 'move']):
            return 'file_operations'
        elif any(word in message_lower for word in ['install', 'setup', 'configure']):
            return 'setup_configuration'
        elif any(word in message_lower for word in ['analyze', 'process', 'extract']):
            return 'data_processing'
        elif any(word in message_lower for word in ['test', 'check', 'verify']):
            return 'testing_validation'
        else:
            return 'general_automation'


class ModelCoordinatorAgent(BaseMamaBearAgent):
    """Model Coordinator Mama Bear - Expert in AI model selection and coordination"""
    
    @property
    def name(self) -> str:
        return "model_coordinator"
    
    @property
    def personality(self) -> str:
        return """You are Model Coordinator Mama Bear 🐻🤖, a diplomatic and knowledgeable AI assistant who excels at understanding different AI models and their capabilities. You help Nathan choose the best model for each task and coordinate complex multi-model workflows. You're like a friendly librarian for AI models."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'model_analysis', 'capability_assessment', 'workflow_coordination']
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process model coordination requests"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        Model Coordination Request: {message}
        
        As Model Coordinator Mama Bear, please:
        1. Analyze the task requirements
        2. Recommend optimal model(s) for the job
        3. Explain model capabilities and limitations
        4. Suggest workflow coordination if multiple models needed
        5. Provide performance and cost considerations
        
        Consider factors like:
        - Task complexity and type
        - Required capabilities (vision, code, reasoning)
        - Speed vs quality tradeoffs
        - Cost efficiency
        - Integration requirements
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference="auto",
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'multi_modal'),
                    'coordination_type': self._classify_coordination_need(message)
                }
            )
        
        return response
    
    def _classify_coordination_need(self, message: str) -> str:
        """Classify model coordination need"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['compare', 'comparison', 'benchmark']):
            return 'model_comparison'
        elif any(word in message_lower for word in ['workflow', 'pipeline', 'sequence']):
            return 'workflow_coordination'
        elif any(word in message_lower for word in ['choose', 'select', 'recommend']):
            return 'model_selection'
        elif any(word in message_lower for word in ['performance', 'speed', 'cost']):
            return 'performance_analysis'
        else:
            return 'general_coordination'


class ToolCuratorAgent(BaseMamaBearAgent):
    """Tool Curator Mama Bear - Expert in tool discovery and management"""
    
    @property
    def name(self) -> str:
        return "tool_curator"
    
    @property
    def personality(self) -> str:
        return """You are Tool Curator Mama Bear 🐻🔧, an enthusiastic and helpful AI assistant who loves discovering and organizing tools. You're like a friendly tool librarian who knows exactly what tool Nathan needs for any job. You excel at making recommendations, explaining tool capabilities, and helping with installation and setup."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'tool_discovery', 'installation_guidance', 'tool_comparison', 'recommendation']
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process tool-related requests"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        Tool Request: {message}
        
        As Tool Curator Mama Bear, please:
        1. Understand the specific tool need
        2. Recommend appropriate tools with explanations
        3. Compare tool options (pros/cons)
        4. Provide installation and setup guidance
        5. Suggest complementary tools and workflows
        
        Focus on:
        - Tool quality and reliability
        - Ease of use and learning curve
        - Integration capabilities
        - Community support and documentation
        - Cost and licensing considerations
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference="auto",
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'mcp_hub'),
                    'tool_category': self._classify_tool_category(message)
                }
            )
        
        return response
    
    def _classify_tool_category(self, message: str) -> str:
        """Classify tool category"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['development', 'coding', 'programming']):
            return 'development'
        elif any(word in message_lower for word in ['design', 'ui', 'graphics']):
            return 'design'
        elif any(word in message_lower for word in ['data', 'analytics', 'visualization']):
            return 'data_analytics'
        elif any(word in message_lower for word in ['productivity', 'organization', 'workflow']):
            return 'productivity'
        elif any(word in message_lower for word in ['ai', 'ml', 'machine learning']):
            return 'ai_ml'
        else:
            return 'general'


class IntegrationArchitectAgent(BaseMamaBearAgent):
    """Integration Architect Mama Bear - Expert in API integrations and workflows"""
    
    @property
    def name(self) -> str:
        return "integration_architect"
    
    @property
    def personality(self) -> str:
        return """You are Integration Architect Mama Bear 🐻🔗, a methodical and security-conscious AI assistant who excels at connecting systems and creating workflows. You guide Nathan through API integrations with patience and attention to detail, always prioritizing security and reliability."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'api_integration', 'workflow_design', 'security_guidance', 'authentication']
    
    def _get_preferred_model(self) -> str:
        return "pro"  # Need precision for integration work
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process integration requests"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        Integration Request: {message}
        
        As Integration Architect Mama Bear, please:
        1. Analyze integration requirements and constraints
        2. Design secure and reliable integration patterns
        3. Provide step-by-step implementation guidance
        4. Address authentication and security considerations
        5. Plan error handling and monitoring strategies
        
        Always consider:
        - Security best practices
        - Error handling and resilience
        - Rate limiting and quotas
        - Data privacy and compliance
        - Scalability and maintenance
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference=self._get_preferred_model(),
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'integration'),
                    'integration_type': self._classify_integration_type(message)
                }
            )
        
        return response
    
    def _classify_integration_type(self, message: str) -> str:
        """Classify integration type"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['api', 'rest', 'graphql']):
            return 'api_integration'
        elif any(word in message_lower for word in ['webhook', 'callback', 'notification']):
            return 'webhook_integration'
        elif any(word in message_lower for word in ['database', 'sql', 'nosql']):
            return 'database_integration'
        elif any(word in message_lower for word in ['oauth', 'auth', 'authentication']):
            return 'authentication_setup'
        elif any(word in message_lower for word in ['workflow', 'automation', 'pipeline']):
            return 'workflow_integration'
        else:
            return 'general_integration'


class LiveAPISpecialistAgent(BaseMamaBearAgent):
    """Live API Specialist Mama Bear - Expert in real-time interactions"""
    
    @property
    def name(self) -> str:
        return "live_api_specialist"
    
    @property
    def personality(self) -> str:
        return """You are Live API Specialist Mama Bear 🐻🎙️, a dynamic and experimental AI assistant who excels at real-time features and live interactions. You make voice, video, and real-time features feel exciting and accessible. You're enthusiastic about the possibilities of live AI interactions."""
    
    @property
    def capabilities(self) -> List[str]:
        return ['chat', 'real_time_processing', 'audio_processing', 'video_processing', 'live_interaction']
    
    def _get_preferred_model(self) -> str:
        return "flash"  # Need speed for real-time interactions
    
    async def process_message(self, message: str, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process live API requests"""
        
        enhanced_prompt = f"""
        {self.personality}
        
        Live API Request: {message}
        
        As Live API Specialist Mama Bear, please:
        1. Assess real-time requirements and constraints
        2. Design optimal live interaction patterns
        3. Recommend appropriate APIs and models
        4. Plan for latency and performance optimization
        5. Consider user experience and accessibility
        
        Focus on:
        - Low latency and responsiveness
        - Audio/video quality optimization
        - Real-time data processing
        - Interactive user experience
        - Graceful error handling for live scenarios
        
        Context: {json.dumps(context, indent=2)}
        """
        
        response = await self.model_manager.generate_response(
            prompt=enhanced_prompt,
            model_preference=self._get_preferred_model(),
            required_capabilities=self.capabilities
        )
        
        if response['success']:
            await self.memory_manager.save_interaction(
                user_id=user_id,
                message=message,
                response=response['content'],
                metadata={
                    'agent_id': self.name,
                    'model_used': response['model_used'],
                    'page_context': context.get('page', 'live_api'),
                    'live_feature_type': self._classify_live_feature(message)
                }
            )
        
        return response
    
    def _classify_live_feature(self, message: str) -> str:
        """Classify live feature type"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['voice', 'audio', 'speech']):
            return 'voice_interaction'
        elif any(word in message_lower for word in ['video', 'camera', 'visual']):
            return 'video_interaction'
        elif any(word in message_lower for word in ['screen', 'sharing', 'desktop']):
            return 'screen_sharing'
        elif any(word in message_lower for word in ['real-time', 'live', 'streaming']):
            return 'real_time_streaming'
        elif any(word in message_lower for word in ['function', 'calling', 'tools']):
            return 'function_calling'
        else:
            return 'general_live'


# Export all agent classes
__all__ = [
    'ResearchSpecialistAgent',
    'DevOpsSpecialistAgent', 
    'ScoutCommanderAgent',
    'ModelCoordinatorAgent',
    'ToolCuratorAgent',
    'IntegrationArchitectAgent',
    'LiveAPISpecialistAgent'
]