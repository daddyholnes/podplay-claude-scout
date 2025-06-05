#!/usr/bin/env python3
"""
🐻 Enhanced Mama Bear Orchestrator
Intelligent agent coordination with Computer Use Agent and MCP Browser integration
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from .enhanced_scrapybara_manager import enhanced_scrapybara
from .mama_bear_memory_system import EnhancedMemoryManager

logger = logging.getLogger(__name__)

class TaskType(Enum):
    RESEARCH = "research"
    BROWSER_AUTOMATION = "browser_automation"
    COMPUTER_USE = "computer_use"
    MULTI_INSTANCE = "multi_instance"
    COLLABORATION = "collaboration"
    ANALYSIS = "analysis"

@dataclass
class AgentTask:
    """Represents a task for Mama Bear agents"""
    task_id: str
    task_type: TaskType
    description: str
    user_id: str
    priority: int = 1
    status: str = "pending"
    created_at: datetime = None
    assigned_agent: str = None
    instance_id: str = None
    progress: Dict[str, Any] = None
    result: Dict[str, Any] = None

class EnhancedMamaBearOrchestrator:
    """Orchestrates multiple Mama Bear agents with enhanced capabilities"""
    
    def __init__(self, memory_manager=None, model_manager=None, scrapybara_client=None):
        self.active_tasks: Dict[str, AgentTask] = {}
        self.agent_pool = {
            'research_specialist': {'status': 'available', 'capabilities': ['research', 'analysis']},
            'browser_automation': {'status': 'available', 'capabilities': ['browser_automation', 'web_scraping']},
            'computer_use_agent': {'status': 'available', 'capabilities': ['computer_use', 'desktop_automation']},
            'collaboration_manager': {'status': 'available', 'capabilities': ['collaboration', 'session_management']},
            'multi_instance_coordinator': {'status': 'available', 'capabilities': ['multi_instance', 'parallel_processing']}
        }
        self.memory_manager = memory_manager or EnhancedMemoryManager()
        self.model_manager = model_manager
        self.scrapybara_client = scrapybara_client
        
    async def submit_task(self, task_description: str, task_type: TaskType, user_id: str, priority: int = 1) -> str:
        """Submit a new task to the orchestrator"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        task = AgentTask(
            task_id=task_id,
            task_type=task_type,
            description=task_description,
            user_id=user_id,
            priority=priority,
            created_at=datetime.now(),
            progress={'status': 'queued', 'steps': []}
        )
        
        self.active_tasks[task_id] = task
        
        # Assign to appropriate agent
        await self._assign_task(task)
        
        logger.info(f"Task submitted: {task_id} - {task_description}")
        return task_id
    
    async def _assign_task(self, task: AgentTask):
        """Assign task to the most suitable agent"""
        best_agent = None
        best_score = 0
        
        for agent_name, agent_info in self.agent_pool.items():
            if agent_info['status'] != 'available':
                continue
                
            # Calculate suitability score
            score = 0
            if task.task_type.value in agent_info['capabilities']:
                score += 10
                
            # Add priority weighting
            score += task.priority
            
            if score > best_score:
                best_score = score
                best_agent = agent_name
        
        if best_agent:
            task.assigned_agent = best_agent
            task.status = "assigned"
            self.agent_pool[best_agent]['status'] = 'busy'
            
            # Execute task asynchronously
            asyncio.create_task(self._execute_task(task))
        else:
            task.status = "waiting"
            logger.warning(f"No available agent for task {task.task_id}")
    
    async def _execute_task(self, task: AgentTask):
        """Execute a task based on its type"""
        try:
            task.status = "executing"
            task.progress['status'] = 'in_progress'
            
            if task.task_type == TaskType.RESEARCH:
                result = await self._execute_research_task(task)
            elif task.task_type == TaskType.BROWSER_AUTOMATION:
                result = await self._execute_browser_task(task)
            elif task.task_type == TaskType.COMPUTER_USE:
                result = await self._execute_computer_use_task(task)
            elif task.task_type == TaskType.MULTI_INSTANCE:
                result = await self._execute_multi_instance_task(task)
            elif task.task_type == TaskType.COLLABORATION:
                result = await self._execute_collaboration_task(task)
            elif task.task_type == TaskType.ANALYSIS:
                result = await self._execute_analysis_task(task)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            task.result = result
            task.status = "completed"
            task.progress['status'] = 'completed'
            
            # Save to memory
            await self.memory_manager.save_task_result(task.user_id, task.task_id, result)
            
        except Exception as e:
            task.status = "failed"
            task.progress['status'] = 'failed'
            task.result = {'error': str(e)}
            logger.error(f"Task {task.task_id} failed: {e}")
        
        finally:
            # Free up the agent
            if task.assigned_agent:
                self.agent_pool[task.assigned_agent]['status'] = 'available'
    
    async def _execute_research_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a research task"""
        task.progress['steps'].append("Starting research...")
        
        # Extract research topics from description
        research_topics = [task.description]  # Simplified - could use NLP to extract multiple topics
        
        result = await enhanced_scrapybara.multi_instance_research(
            research_topics=research_topics,
            user_id=task.user_id
        )
        
        task.progress['steps'].append("Research completed")
        return result
    
    async def _execute_browser_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a browser automation task"""
        task.progress['steps'].append("Creating browser session...")
        
        # Create shared browser session
        session = await enhanced_scrapybara.create_shared_browser_session(
            user_id=task.user_id,
            initial_url="https://google.com"
        )
        
        task.instance_id = session.instance_id
        task.progress['steps'].append(f"Browser session created: {session.session_id}")
        
        # Execute browser actions
        result = await enhanced_scrapybara.execute_browser_action(
            session_id=session.session_id,
            action=task.description,
            user_id=task.user_id
        )
        
        task.progress['steps'].append("Browser automation completed")
        return result
    
    async def _execute_computer_use_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a computer use agent task"""
        task.progress['steps'].append("Starting computer use agent...")
        
        # Start new instance for computer use
        instance = await enhanced_scrapybara.client.start_ubuntu()
        task.instance_id = instance.id
        
        task.progress['steps'].append(f"Instance created: {instance.id}")
        
        # Execute computer use task
        result = await enhanced_scrapybara.computer_use_agent_task(
            instance_id=instance.id,
            task_description=task.description
        )
        
        task.progress['steps'].append("Computer use task completed")
        return result
    
    async def _execute_multi_instance_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a multi-instance parallel task"""
        task.progress['steps'].append("Starting multi-instance execution...")
        
        # Parse task for multiple subtasks
        # This is simplified - could use NLP to break down complex tasks
        subtasks = [task.description]  # For now, treat as single task
        
        result = await enhanced_scrapybara.multi_instance_research(
            research_topics=subtasks,
            user_id=task.user_id
        )
        
        task.progress['steps'].append("Multi-instance execution completed")
        return result
    
    async def _execute_collaboration_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a collaboration task"""
        task.progress['steps'].append("Setting up collaboration session...")
        
        # Create shared session
        session = await enhanced_scrapybara.create_shared_browser_session(
            user_id=task.user_id
        )
        
        task.instance_id = session.instance_id
        task.progress['steps'].append(f"Collaboration session: {session.session_id}")
        
        # Return session info for user to join
        return {
            'session_id': session.session_id,
            'instance_id': session.instance_id,
            'join_url': f"/collaborate/{session.session_id}",
            'created_at': session.created_at.isoformat()
        }
    
    async def _execute_analysis_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute an analysis task"""
        task.progress['steps'].append("Starting analysis...")
        
        # Create instance for analysis
        instance = await enhanced_scrapybara.client.start_ubuntu()
        task.instance_id = instance.id
        
        # Take screenshot and analyze
        result = await enhanced_scrapybara.intelligent_screenshot_analysis(
            instance_id=instance.id,
            analysis_request=task.description
        )
        
        task.progress['steps'].append("Analysis completed")
        return result
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task"""
        if task_id not in self.active_tasks:
            return None
            
        task = self.active_tasks[task_id]
        return {
            'task_id': task.task_id,
            'status': task.status,
            'progress': task.progress,
            'assigned_agent': task.assigned_agent,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'description': task.description,
            'result': task.result
        }
    
    async def list_user_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """List all tasks for a user"""
        user_tasks = [
            task for task in self.active_tasks.values() 
            if task.user_id == user_id
        ]
        
        return [
            {
                'task_id': task.task_id,
                'status': task.status,
                'description': task.description,
                'task_type': task.task_type.value,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'assigned_agent': task.assigned_agent
            }
            for task in user_tasks
        ]
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        if task_id not in self.active_tasks:
            return False
            
        task = self.active_tasks[task_id]
        
        if task.status in ['completed', 'failed']:
            return False
            
        task.status = 'cancelled'
        
        # Free up agent if assigned
        if task.assigned_agent:
            self.agent_pool[task.assigned_agent]['status'] = 'available'
        
        logger.info(f"Task cancelled: {task_id}")
        return True
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            'agents': dict(self.agent_pool),
            'active_tasks': len([t for t in self.active_tasks.values() if t.status in ['executing', 'assigned']]),
            'total_tasks': len(self.active_tasks),
            'timestamp': datetime.now().isoformat()
        }

# Global orchestrator instance
mama_bear_orchestrator = EnhancedMamaBearOrchestrator()