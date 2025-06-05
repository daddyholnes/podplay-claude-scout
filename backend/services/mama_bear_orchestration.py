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
import uuid

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class AgentType(Enum):
    RESEARCH_SPECIALIST = "research_specialist"
    DEVOPS_SPECIALIST = "devops_specialist"
    SCOUT_COMMANDER = "scout_commander"
    MODEL_COORDINATOR = "model_coordinator"
    TOOL_CURATOR = "tool_curator"
    INTEGRATION_ARCHITECT = "integration_architect"
    LIVE_API_SPECIALIST = "live_api_specialist"

@dataclass
class Task:
    id: str
    title: str
    description: str
    agent_type: AgentType
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    user_id: str
    context: Dict[str, Any]
    dependencies: List[str] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class AgentPlan:
    id: str
    title: str
    description: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    status: str
    subtasks: List[Dict[str, Any]]
    context: Dict[str, Any]
    estimated_total_duration: Optional[int] = None
    progress_percentage: float = 0.0

class WorkflowEngine:
    """Advanced workflow engine for orchestrating complex multi-agent tasks"""
    
    def __init__(self):
        self.workflows = {}
        self.active_executions = {}
        self.workflow_templates = {}
        
    async def create_workflow(self, name: str, steps: List[Dict], context: Dict = None):
        """Create a new workflow definition"""
        workflow_id = str(uuid.uuid4())
        workflow = {
            'id': workflow_id,
            'name': name,
            'steps': steps,
            'context': context or {},
            'created_at': datetime.now().isoformat()
        }
        self.workflows[workflow_id] = workflow
        return workflow_id
    
    async def execute_workflow(self, workflow_id: str, input_data: Dict = None):
        """Execute a workflow with given input data"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution_id = str(uuid.uuid4())
        execution = {
            'id': execution_id,
            'workflow_id': workflow_id,
            'status': 'running',
            'input_data': input_data or {},
            'current_step': 0,
            'results': {},
            'started_at': datetime.now().isoformat()
        }
        
        self.active_executions[execution_id] = execution
        
        # Start execution in background
        asyncio.create_task(self._run_workflow_execution(execution_id))
        
        return execution_id
    
    async def _run_workflow_execution(self, execution_id: str):
        """Internal method to run workflow execution"""
        execution = self.active_executions[execution_id]
        workflow = self.workflows[execution['workflow_id']]
        
        try:
            for i, step in enumerate(workflow['steps']):
                execution['current_step'] = i
                
                # Execute step
                result = await self._execute_workflow_step(step, execution)
                execution['results'][f'step_{i}'] = result
                
                # Check if step failed
                if not result.get('success', False):
                    execution['status'] = 'failed'
                    execution['error'] = result.get('error')
                    break
            
            if execution['status'] != 'failed':
                execution['status'] = 'completed'
                execution['completed_at'] = datetime.now().isoformat()
                
        except Exception as e:
            execution['status'] = 'failed'
            execution['error'] = str(e)
            logger.error(f"Workflow execution {execution_id} failed: {e}")
    
    async def _execute_workflow_step(self, step: Dict, execution: Dict):
        """Execute a single workflow step"""
        # This would integrate with the actual agent execution
        # For now, simulate execution
        await asyncio.sleep(1)
        return {'success': True, 'data': f"Step {step.get('name')} completed"}

class AgentOrchestrator:
    """
    🐻 Central orchestrator for all Mama Bear agents
    Manages agent collaboration, context sharing, and intelligent task routing
    """
    
    def __init__(self, memory_manager, model_manager, scrapybara_client):
        self.memory_manager = memory_manager
        self.model_manager = model_manager
        self.scrapybara_client = scrapybara_client
        
        # Core orchestration components
        self.task_queue = asyncio.Queue()
        self.active_tasks = {}
        self.completed_tasks = {}
        self.agent_registry = {}
        self.context_manager = ContextManager()
        self.workflow_engine = WorkflowEngine()
        
        # Plan storage
        self._plans: Dict[str, AgentPlan] = {}
        
        # Performance tracking
        self.metrics = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'average_response_time': 0,
            'agent_utilization': defaultdict(float)
        }
        
        # Real-time updates
        self.update_callbacks = []
        
    def register_agent(self, agent_type: AgentType, agent_instance):
        """Register an agent with the orchestrator"""
        self.agent_registry[agent_type] = agent_instance
        logger.info(f"🐻 Registered agent: {agent_type.value}")
    
    async def create_plan(self, title: str, description: str, user_id: str, context: Dict = None) -> Dict[str, Any]:
        """Create a comprehensive agent plan"""
        try:
            plan_id = str(uuid.uuid4())
            
            # Analyze the request to determine optimal subtasks
            subtasks = await self._analyze_and_create_subtasks(description, context or {})
            
            plan = AgentPlan(
                id=plan_id,
                title=title,
                description=description,
                user_id=user_id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status="pending",
                subtasks=subtasks,
                context=context or {},
                estimated_total_duration=sum(task.get('estimated_duration', 300) for task in subtasks)
            )
            
            self._plans[plan_id] = plan
            
            # Notify subscribers
            await self._notify_plan_created(plan)
            
            return asdict(plan)
            
        except Exception as e:
            logger.error(f"Error creating plan: {e}")
            raise
    
    async def _analyze_and_create_subtasks(self, description: str, context: Dict) -> List[Dict[str, Any]]:
        """Analyze request and create optimal subtasks"""
        
        # Use the model manager to analyze the request
        analysis_prompt = f"""
        Analyze this request and break it down into specific subtasks:
        
        Request: {description}
        Context: {json.dumps(context, indent=2)}
        
        Create subtasks that can be handled by these agent types:
        - research_specialist: Research, analysis, information gathering
        - devops_specialist: Infrastructure, deployment, system management
        - scout_commander: Autonomous execution, file operations, automation
        - model_coordinator: AI model selection and coordination
        - tool_curator: Tool discovery, installation, management
        - integration_architect: API integrations, workflow creation
        - live_api_specialist: Real-time interactions, voice/video processing
        
        Return a JSON array of subtasks with:
        - id: unique identifier
        - title: clear task title
        - description: detailed description
        - agent: agent type to handle this task
        - priority: low/medium/high/urgent
        - estimated_duration: seconds
        - dependencies: array of subtask IDs this depends on
        """
        
        try:
            # Get analysis from the model
            response = await self.model_manager.generate_response(
                prompt=analysis_prompt,
                model_preference="pro"  # Use the most capable model
            )
            
            # Parse the response as JSON
            subtasks_data = json.loads(response.get('content', '[]'))
            
            # Validate and enhance subtasks
            enhanced_subtasks = []
            for i, task_data in enumerate(subtasks_data):
                enhanced_task = {
                    'id': task_data.get('id', f"subtask_{i}"),
                    'title': task_data.get('title', f"Subtask {i+1}"),
                    'description': task_data.get('description', ''),
                    'agent': task_data.get('agent', 'research_specialist'),
                    'priority': task_data.get('priority', 'medium'),
                    'status': 'pending',
                    'estimated_duration': task_data.get('estimated_duration', 300),
                    'dependencies': task_data.get('dependencies', []),
                    'created_at': datetime.now().isoformat()
                }
                enhanced_subtasks.append(enhanced_task)
            
            return enhanced_subtasks
            
        except Exception as e:
            logger.error(f"Error analyzing subtasks: {e}")
            # Fallback to simple single task
            return [{
                'id': 'main_task',
                'title': 'Execute Request',
                'description': description,
                'agent': 'research_specialist',
                'priority': 'medium',
                'status': 'pending',
                'estimated_duration': 600,
                'dependencies': [],
                'created_at': datetime.now().isoformat()
            }]
    
    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        """Retrieve a plan by ID"""
        if plan_id not in self._plans:
            raise ValueError(f"Plan {plan_id} not found")
        return asdict(self._plans[plan_id])
    
    def store_plan(self, plan: Dict[str, Any]):
        """Store or update a plan"""
        plan_id = plan['id']
        # Convert dict back to AgentPlan object
        plan_obj = AgentPlan(**plan)
        plan_obj.updated_at = datetime.now()
        self._plans[plan_id] = plan_obj
    
    async def run_subtask(self, plan_id: str, subtask_id: str, user_id: str) -> Dict[str, Any]:
        """Execute a specific subtask"""
        try:
            plan_dict = self.get_plan(plan_id)
            subtask = next((s for s in plan_dict['subtasks'] if s['id'] == subtask_id), None)
            
            if not subtask:
                return {'success': False, 'error': 'Subtask not found'}
            
            if subtask['status'] not in ['pending', 'paused']:
                return {'success': False, 'error': 'Subtask not runnable'}
            
            # Update subtask status
            subtask['status'] = 'in_progress'
            subtask['started_by'] = user_id
            subtask['started_at'] = datetime.now().isoformat()
            
            # Store updated plan
            self.store_plan(plan_dict)
            
            # Execute subtask asynchronously
            asyncio.create_task(self._execute_subtask(plan_id, subtask_id, subtask))
            
            return {'success': True, 'subtask': subtask}
            
        except Exception as e:
            logger.error(f"Error running subtask: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_subtask(self, plan_id: str, subtask_id: str, subtask: Dict[str, Any]):
        """Internal method to execute a subtask"""
        try:
            logger.info(f"🐻 Executing subtask {subtask_id} with agent {subtask['agent']}")
            
            # Get the appropriate agent
            agent_type = AgentType(subtask['agent'])
            agent = self.agent_registry.get(agent_type)
            
            if not agent:
                raise ValueError(f"Agent {subtask['agent']} not available")
            
            # Execute the subtask
            result = await agent.execute_task(
                task_description=subtask['description'],
                context=subtask.get('context', {}),
                priority=subtask.get('priority', 'medium')
            )
            
            # Update subtask with result
            plan_dict = self.get_plan(plan_id)
            subtask = next((s for s in plan_dict['subtasks'] if s['id'] == subtask_id), None)
            
            if result.get('success', False):
                subtask['status'] = 'completed'
                subtask['result'] = result
            else:
                subtask['status'] = 'failed'
                subtask['error'] = result.get('error', 'Unknown error')
            
            subtask['completed_at'] = datetime.now().isoformat()
            
            # Store updated plan
            self.store_plan(plan_dict)
            
            # Update metrics
            self.metrics['tasks_completed'] += 1
            
            # Notify subscribers
            await self._notify_subtask_completed(plan_id, subtask_id, subtask)
            
            logger.info(f"✅ Subtask {subtask_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Subtask {subtask_id} failed: {e}")
            
            # Update subtask with error
            plan_dict = self.get_plan(plan_id)
            subtask = next((s for s in plan_dict['subtasks'] if s['id'] == subtask_id), None)
            subtask['status'] = 'failed'
            subtask['error'] = str(e)
            subtask['completed_at'] = datetime.now().isoformat()
            
            self.store_plan(plan_dict)
            self.metrics['tasks_failed'] += 1
    
    async def pause_subtask(self, plan_id: str, subtask_id: str, user_id: str) -> Dict[str, Any]:
        """Pause a running subtask"""
        try:
            plan_dict = self.get_plan(plan_id)
            subtask = next((s for s in plan_dict['subtasks'] if s['id'] == subtask_id), None)
            
            if not subtask:
                return {'success': False, 'error': 'Subtask not found'}
            
            if subtask['status'] != 'in_progress':
                return {'success': False, 'error': 'Subtask not in progress'}
            
            subtask['status'] = 'paused'
            subtask['paused_by'] = user_id
            subtask['paused_at'] = datetime.now().isoformat()
            
            self.store_plan(plan_dict)
            
            return {'success': True, 'subtask': subtask}
            
        except Exception as e:
            logger.error(f"Error pausing subtask: {e}")
            return {'success': False, 'error': str(e)}
    
    async def reassign_subtask(self, plan_id: str, subtask_id: str, new_agent: str, user_id: str) -> Dict[str, Any]:
        """Reassign a subtask to a different agent"""
        try:
            plan_dict = self.get_plan(plan_id)
            subtask = next((s for s in plan_dict['subtasks'] if s['id'] == subtask_id), None)
            
            if not subtask:
                return {'success': False, 'error': 'Subtask not found'}
            
            subtask['agent'] = new_agent
            subtask['reassigned_by'] = user_id
            subtask['reassigned_at'] = datetime.now().isoformat()
            
            self.store_plan(plan_dict)
            
            return {'success': True, 'subtask': subtask}
            
        except Exception as e:
            logger.error(f"Error reassigning subtask: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_orchestration_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestration status"""
        return {
            'active_plans': len(self._plans),
            'registered_agents': len(self.agent_registry),
            'metrics': self.metrics,
            'system_health': 'healthy'  # TODO: Implement health checks
        }
    
    async def _notify_plan_created(self, plan: AgentPlan):
        """Notify subscribers about plan creation"""
        for callback in self.update_callbacks:
            try:
                await callback('plan_created', asdict(plan))
            except Exception as e:
                logger.error(f"Error in update callback: {e}")
    
    async def _notify_subtask_completed(self, plan_id: str, subtask_id: str, subtask: Dict):
        """Notify subscribers about subtask completion"""
        for callback in self.update_callbacks:
            try:
                await callback('subtask_completed', {
                    'plan_id': plan_id,
                    'subtask_id': subtask_id,
                    'subtask': subtask
                })
            except Exception as e:
                logger.error(f"Error in update callback: {e}")
    
    def add_update_callback(self, callback: Callable):
        """Add a callback for real-time updates"""
        self.update_callbacks.append(callback)


class ContextManager:
    """Manages context sharing between agents"""
    
    def __init__(self):
        self.contexts = {}
        self.shared_state = {}
    
    async def get_context(self, user_id: str, session_id: str = None) -> Dict[str, Any]:
        """Get context for a user/session"""
        key = f"{user_id}:{session_id}" if session_id else user_id
        return self.contexts.get(key, {})
    
    async def update_context(self, user_id: str, context_update: Dict[str, Any], session_id: str = None):
        """Update context for a user/session"""
        key = f"{user_id}:{session_id}" if session_id else user_id
        if key not in self.contexts:
            self.contexts[key] = {}
        self.contexts[key].update(context_update)
    
    async def share_context(self, from_agent: str, to_agent: str, context_data: Dict[str, Any]):
        """Share context between agents"""
        share_key = f"{from_agent}:{to_agent}"
        self.shared_state[share_key] = {
            'data': context_data,
            'timestamp': datetime.now().isoformat()
        }


async def initialize_orchestration(memory_manager, model_manager, scrapybara_client):
    """Initialize the orchestration system"""
    orchestrator = AgentOrchestrator(memory_manager, model_manager, scrapybara_client)
    
    # Set up any additional configuration
    logger.info("🐻 Agent Orchestration System initialized")
    
    return orchestrator