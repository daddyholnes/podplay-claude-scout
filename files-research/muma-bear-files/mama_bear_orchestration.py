# backend/services/mama_bear_orchestration.py
"""
🐻 Mama Bear Agent Orchestration System
Core logic for agent collaboration, context awareness, and workflow management
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    WAITING = "waiting"
    COLLABORATING = "collaborating"
    ERROR = "error"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentContext:
    """What each agent knows about the current situation"""
    agent_id: str
    current_task: Optional[str] = None
    user_intent: str = ""
    project_context: Dict[str, Any] = None
    conversation_history: List[Dict] = None
    available_tools: List[str] = None
    resource_limits: Dict[str, Any] = None
    collaboration_state: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.project_context is None:
            self.project_context = {}
        if self.conversation_history is None:
            self.conversation_history = []
        if self.available_tools is None:
            self.available_tools = []
        if self.resource_limits is None:
            self.resource_limits = {}
        if self.collaboration_state is None:
            self.collaboration_state = {}

@dataclass
class Task:
    """Represents a task that can be executed by agents"""
    id: str
    title: str
    description: str
    agent_type: str
    priority: TaskPriority
    status: TaskStatus
    dependencies: List[str] = None
    estimated_duration: int = 300  # seconds
    max_retries: int = 3
    current_attempt: int = 0
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}

@dataclass
class Plan:
    """A collection of tasks with dependencies and execution strategy"""
    id: str
    title: str
    description: str
    tasks: List[Task]
    user_id: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    estimated_completion: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class AgentCapability(ABC):
    """Base class for agent capabilities"""
    
    @abstractmethod
    async def can_handle(self, task: Task, context: AgentContext) -> bool:
        """Check if this capability can handle the given task"""
        pass
    
    @abstractmethod
    async def execute(self, task: Task, context: AgentContext) -> Dict[str, Any]:
        """Execute the task and return results"""
        pass

class ContextAwareness:
    """Manages what agents know about the current situation"""
    
    def __init__(self, memory_manager, model_manager):
        self.memory = memory_manager
        self.model_manager = model_manager
        self.global_context = {}
        self.agent_contexts = {}
        
    async def update_global_context(self, key: str, value: Any):
        """Update global context that all agents can access"""
        self.global_context[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'source': 'system'
        }
        
        # Persist important context to memory
        if key in ['user_intent', 'project_state', 'active_plan']:
            await self.memory.save_context(key, value)
    
    async def get_agent_context(self, agent_id: str) -> AgentContext:
        """Get complete context for a specific agent"""
        if agent_id not in self.agent_contexts:
            self.agent_contexts[agent_id] = AgentContext(agent_id=agent_id)
        
        context = self.agent_contexts[agent_id]
        
        # Enrich context with relevant global information
        context.user_intent = self.global_context.get('user_intent', {}).get('value', '')
        context.project_context = self.global_context.get('project_state', {}).get('value', {})
        
        # Get recent conversation history from memory
        context.conversation_history = await self.memory.get_recent_conversations(
            agent_id=agent_id, 
            limit=10
        )
        
        # Get available tools and resources
        context.available_tools = await self._get_available_tools(agent_id)
        context.resource_limits = await self._get_resource_limits(agent_id)
        
        return context
    
    async def _get_available_tools(self, agent_id: str) -> List[str]:
        """Get tools available to this agent"""
        agent_type = agent_id.split('_')[0]  # e.g., 'scout_agent_1' -> 'scout'
        
        tool_mapping = {
            'scout': ['scrapybara', 'web_search', 'document_analysis', 'github_api'],
            'mama_bear': ['code_generation', 'planning', 'review', 'coordination'],
            'model_manager': ['model_selection', 'fine_tuning', 'deployment', 'monitoring'],
            'monitor': ['resource_tracking', 'alerting', 'quota_management', 'billing'],
            'planner': ['task_decomposition', 'dependency_analysis', 'estimation', 'optimization']
        }
        
        return tool_mapping.get(agent_type, [])
    
    async def _get_resource_limits(self, agent_id: str) -> Dict[str, Any]:
        """Get resource limits for this agent"""
        # Check current quota status from model manager
        model_status = self.model_manager.get_model_status()
        
        return {
            'api_quota_remaining': sum(
                model['quota_limit'] - model['quota_used'] 
                for model in model_status['models']
            ),
            'scrapybara_instances': 5,  # Max concurrent instances
            'memory_limit_mb': 1024,
            'execution_timeout': 3600  # 1 hour max execution
        }

class AgentOrchestrator:
    """Orchestrates collaboration between different Mama Bear agents"""
    
    def __init__(self, memory_manager, model_manager, scrapybara_client):
        self.memory = memory_manager
        self.model_manager = model_manager
        self.scrapybara = scrapybara_client
        self.context_awareness = ContextAwareness(memory_manager, model_manager)
        
        # Agent registry
        self.agents = {}
        self.active_tasks = {}
        self.task_queue = deque()
        self.completed_tasks = {}
        
        # Communication channels
        self.agent_messages = defaultdict(deque)
        self.collaboration_sessions = {}
        
        # Initialize specialized agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all Mama Bear agent types"""
        from mama_bear_specialized_variants import (
            ResearchSpecialist, DevOpsSpecialist, ScoutCommander,
            ModelCoordinator, ToolCurator, IntegrationArchitect, LiveAPISpecialist
        )
        
        self.agents = {
            'research_specialist': MamaBearAgent('research_specialist', ResearchSpecialist(), self),
            'devops_specialist': MamaBearAgent('devops_specialist', DevOpsSpecialist(), self),
            'scout_commander': MamaBearAgent('scout_commander', ScoutCommander(), self),
            'model_coordinator': MamaBearAgent('model_coordinator', ModelCoordinator(), self),
            'tool_curator': MamaBearAgent('tool_curator', ToolCurator(), self),
            'integration_architect': MamaBearAgent('integration_architect', IntegrationArchitect(), self),
            'live_api_specialist': MamaBearAgent('live_api_specialist', LiveAPISpecialist(), self),
            'lead_developer': LeadDeveloperAgent('lead_developer', self)  # Master coordinator
        }
    
    async def process_user_request(self, message: str, user_id: str, page_context: str = 'main_chat') -> Dict[str, Any]:
        """Main entry point for user requests - determines which agents to involve"""
        
        # Update global context with user intent
        await self.context_awareness.update_global_context('user_intent', message)
        await self.context_awareness.update_global_context('user_id', user_id)
        await self.context_awareness.update_global_context('page_context', page_context)
        
        # Analyze request to determine optimal agent strategy
        strategy = await self._analyze_request(message, page_context)
        
        if strategy['type'] == 'simple_response':
            # Single agent can handle this
            agent = self.agents[strategy['primary_agent']]
            return await agent.handle_request(message, user_id)
            
        elif strategy['type'] == 'collaborative':
            # Multiple agents need to collaborate
            return await self._orchestrate_collaboration(strategy, message, user_id)
            
        elif strategy['type'] == 'plan_and_execute':
            # Need planning phase followed by execution
            return await self._plan_and_execute(strategy, message, user_id)
    
    async def _analyze_request(self, message: str, page_context: str) -> Dict[str, Any]:
        """Analyze user request to determine optimal agent strategy"""
        
        # Use the research specialist to analyze the request
        analysis_prompt = f"""
        Analyze this user request and determine the optimal agent strategy:
        
        Request: "{message}"
        Context: {page_context}
        
        Classify as:
        1. simple_response - One agent can handle this (specify which agent)
        2. collaborative - Multiple agents need to work together (specify agents and roles)
        3. plan_and_execute - Needs planning phase then execution (specify planning steps)
        
        Consider:
        - Complexity of the request
        - Required capabilities (coding, research, deployment, etc.)
        - Time sensitivity
        - Resource requirements
        
        Return a JSON strategy object.
        """
        
        # Get analysis from model manager
        result = await self.model_manager.get_response(
            prompt=analysis_prompt,
            mama_bear_variant='research_specialist',
            required_capabilities=['chat', 'code']
        )
        
        if result['success']:
            try:
                # Parse the strategy from the response
                strategy = self._extract_strategy_from_response(result['response'])
                return strategy
            except:
                # Fallback to simple routing based on page context
                return self._fallback_strategy(page_context)
        else:
            return self._fallback_strategy(page_context)
    
    def _extract_strategy_from_response(self, response: str) -> Dict[str, Any]:
        """Extract strategy object from AI response"""
        # Try to find JSON in the response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback: analyze keywords in response
        if 'simple' in response.lower():
            if 'research' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'research_specialist'}
            elif 'code' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'lead_developer'}
            elif 'deploy' in response.lower():
                return {'type': 'simple_response', 'primary_agent': 'devops_specialist'}
        
        # Default to lead developer
        return {'type': 'simple_response', 'primary_agent': 'lead_developer'}
    
    def _fallback_strategy(self, page_context: str) -> Dict[str, Any]:
        """Fallback strategy based on page context"""
        agent_mapping = {
            'main_chat': 'research_specialist',
            'vm_hub': 'devops_specialist',
            'scout': 'scout_commander',
            'multi_modal': 'model_coordinator',
            'mcp_hub': 'tool_curator',
            'integration': 'integration_architect',
            'live_api': 'live_api_specialist'
        }
        
        return {
            'type': 'simple_response',
            'primary_agent': agent_mapping.get(page_context, 'lead_developer')
        }
    
    async def _orchestrate_collaboration(self, strategy: Dict[str, Any], message: str, user_id: str) -> Dict[str, Any]:
        """Orchestrate collaboration between multiple agents"""
        
        collaboration_id = f"collab_{datetime.now().timestamp()}"
        self.collaboration_sessions[collaboration_id] = {
            'agents': strategy.get('agents', []),
            'roles': strategy.get('roles', {}),
            'status': 'active',
            'started_at': datetime.now(),
            'messages': []
        }
        
        # Create tasks for each agent
        tasks = []
        for i, (agent_id, role) in enumerate(strategy.get('roles', {}).items()):
            task = Task(
                id=f"{collaboration_id}_task_{i}",
                title=f"Collaborative task for {agent_id}",
                description=f"Role: {role}\nOriginal request: {message}",
                agent_type=agent_id,
                priority=TaskPriority.HIGH,
                status=TaskStatus.PENDING,
                context={'collaboration_id': collaboration_id, 'role': role}
            )
            tasks.append(task)
        
        # Execute tasks concurrently
        results = await asyncio.gather(
            *[self._execute_task(task) for task in tasks],
            return_exceptions=True
        )
        
        # Synthesize results
        return await self._synthesize_collaboration_results(collaboration_id, results, message)
    
    async def _plan_and_execute(self, strategy: Dict[str, Any], message: str, user_id: str) -> Dict[str, Any]:
        """Plan and execute complex multi-step requests"""
        
        # Phase 1: Planning
        planner_agent = self.agents.get('lead_developer')  # Lead developer acts as planner
        plan = await planner_agent.create_plan(message, user_id)
        
        # Present plan to user for approval (in real implementation, you'd wait for user input)
        # For now, we'll auto-approve simple plans
        
        # Phase 2: Execution
        if plan['status'] == 'approved':
            return await self._execute_plan(plan, user_id)
        else:
            return {
                'type': 'plan_proposal',
                'plan': plan,
                'message': "I've created a plan for your request. Would you like me to proceed?"
            }
    
    async def _execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task with the appropriate agent"""
        
        agent = self.agents.get(task.agent_type)
        if not agent:
            return {'success': False, 'error': f'Agent {task.agent_type} not found'}
        
        # Get context for the agent
        context = await self.context_awareness.get_agent_context(agent.id)
        context.current_task = task.id
        
        # Update task status
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        self.active_tasks[task.id] = task
        
        try:
            # Execute the task
            result = await agent.execute_task(task, context)
            
            # Update task status
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            self.completed_tasks[task.id] = task
            
            return result
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.current_attempt += 1
            
            # Retry if under limit
            if task.current_attempt < task.max_retries:
                logger.warning(f"Task {task.id} failed, retrying ({task.current_attempt}/{task.max_retries})")
                return await self._execute_task(task)
            else:
                logger.error(f"Task {task.id} failed permanently: {e}")
                return {'success': False, 'error': str(e)}
        
        finally:
            # Clean up
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
    
    async def _synthesize_collaboration_results(self, collaboration_id: str, results: List[Dict], original_message: str) -> Dict[str, Any]:
        """Combine results from multiple agents into a coherent response"""
        
        synthesis_prompt = f"""
        Combine these results from different Mama Bear specialists into a coherent response:
        
        Original request: "{original_message}"
        
        Results:
        {json.dumps(results, indent=2)}
        
        Create a unified response that:
        1. Addresses the original request completely
        2. Integrates insights from all specialists
        3. Provides clear next steps if applicable
        4. Maintains Mama Bear's caring, supportive tone
        
        Return a natural, conversational response.
        """
        
        # Use lead developer to synthesize
        result = await self.model_manager.get_response(
            prompt=synthesis_prompt,
            mama_bear_variant='main_chat',
            required_capabilities=['chat']
        )
        
        return {
            'type': 'collaborative_response',
            'content': result['response'] if result['success'] else "I've gathered information from my specialists and I'm ready to help!",
            'collaboration_id': collaboration_id,
            'participating_agents': [r.get('agent_id') for r in results if isinstance(r, dict)],
            'model_used': result.get('model_used'),
            'metadata': {
                'collaboration_results': results,
                'synthesis_successful': result['success']
            }
        }
    
    async def send_agent_message(self, from_agent: str, to_agent: str, message: str, context: Dict = None):
        """Enable agents to communicate with each other"""
        
        message_obj = {
            'from': from_agent,
            'to': to_agent,
            'message': message,
            'context': context or {},
            'timestamp': datetime.now()
        }
        
        self.agent_messages[to_agent].append(message_obj)
        
        # Notify receiving agent if it's currently active
        if to_agent in self.active_tasks:
            agent = self.agents[to_agent]
            await agent.handle_message(message_obj)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = {
                'state': agent.state.value,
                'current_task': agent.current_task,
                'last_activity': agent.last_activity,
                'message_queue_size': len(self.agent_messages[agent_id])
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': agent_statuses,
            'active_tasks': len(self.active_tasks),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'model_manager_status': self.model_manager.get_model_status(),
            'global_context': list(self.context_awareness.global_context.keys())
        }

class MamaBearAgent:
    """Base class for all Mama Bear agents"""
    
    def __init__(self, agent_id: str, specialist_variant, orchestrator):
        self.id = agent_id
        self.variant = specialist_variant
        self.orchestrator = orchestrator
        self.state = AgentState.IDLE
        self.current_task = None
        self.last_activity = datetime.now()
        self.capabilities = []
    
    async def handle_request(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle a direct user request"""
        
        self.state = AgentState.THINKING
        self.last_activity = datetime.now()
        
        try:
            # Get context
            context = await self.orchestrator.context_awareness.get_agent_context(self.id)
            
            # Get system prompt from variant
            system_prompt = self.variant.get_system_prompt()
            
            # Build full prompt
            full_prompt = f"""
            {system_prompt}
            
            Current context:
            - User: {user_id}
            - Previous conversation: {context.conversation_history[-3:] if context.conversation_history else 'None'}
            - Available tools: {context.available_tools}
            - Project context: {context.project_context}
            
            User request: {message}
            
            Please respond as this Mama Bear specialist.
            """
            
            # Get response using model manager
            result = await self.orchestrator.model_manager.get_response(
                prompt=full_prompt,
                mama_bear_variant=self.id.split('_')[0],  # e.g., 'research' from 'research_specialist'
                required_capabilities=['chat']
            )
            
            self.state = AgentState.IDLE
            
            if result['success']:
                # Save interaction to memory
                await self.orchestrator.memory.save_interaction(
                    user_id=user_id,
                    message=message,
                    response=result['response'],
                    metadata={
                        'agent_id': self.id,
                        'model_used': result['model_used']
                    }
                )
                
                return {
                    'success': True,
                    'content': result['response'],
                    'agent_id': self.id,
                    'model_used': result['model_used'],
                    'metadata': result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'content': "I'm having trouble accessing my models right now. Let me try a different approach!",
                    'error': result.get('error'),
                    'agent_id': self.id
                }
                
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Agent {self.id} error: {e}")
            return {
                'success': False,
                'content': "I encountered an error, but I'm working on fixing it! 🐻",
                'error': str(e),
                'agent_id': self.id
            }
    
    async def execute_task(self, task: Task, context: AgentContext) -> Dict[str, Any]:
        """Execute a specific task"""
        
        self.state = AgentState.WORKING
        self.current_task = task.id
        self.last_activity = datetime.now()
        
        # Task-specific logic would go here
        # For now, delegate to handle_request
        return await self.handle_request(task.description, context.user_intent)
    
    async def handle_message(self, message: Dict[str, Any]):
        """Handle messages from other agents"""
        
        # Process inter-agent communication
        logger.info(f"Agent {self.id} received message from {message['from']}: {message['message']}")
        
        # Could trigger collaborative actions here

class LeadDeveloperAgent(MamaBearAgent):
    """Special agent that coordinates other agents and handles complex planning"""
    
    def __init__(self, agent_id: str, orchestrator):
        super().__init__(agent_id, None, orchestrator)
        self.capabilities = ['planning', 'coordination', 'code_review', 'architecture']
    
    async def create_plan(self, request: str, user_id: str) -> Dict[str, Any]:
        """Create a detailed plan for complex requests"""
        
        planning_prompt = f"""
        As the Lead Developer Mama Bear, create a detailed plan for this request:
        
        Request: "{request}"
        User: {user_id}
        
        Break this down into:
        1. Requirements analysis
        2. Task decomposition
        3. Agent assignments
        4. Dependencies
        5. Estimated timeline
        6. Resource requirements
        
        Format as a structured plan that can be executed step by step.
        """
        
        result = await self.orchestrator.model_manager.get_response(
            prompt=planning_prompt,
            mama_bear_variant='main_chat',
            required_capabilities=['chat', 'code']
        )
        
        if result['success']:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': result['response'],
                'status': 'pending_approval',
                'created_by': self.id,
                'user_id': user_id
            }
        else:
            return {
                'id': f"plan_{datetime.now().timestamp()}",
                'title': f"Plan for: {request[:50]}...",
                'description': "I'll help you with this step by step!",
                'status': 'simple',
                'created_by': self.id,
                'user_id': user_id
            }

# Integration function for existing Flask app
async def initialize_orchestration(app, memory_manager, model_manager, scrapybara_client):
    """Initialize the orchestration system and attach to Flask app"""
    
    orchestrator = AgentOrchestrator(memory_manager, model_manager, scrapybara_client)
    app.mama_bear_orchestrator = orchestrator
    
    # Start background tasks
    asyncio.create_task(orchestrator._monitor_system_health())
    
    logger.info("🐻 Mama Bear Orchestration System initialized successfully!")
    return orchestrator