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
        self.update_callbacks = []
    
# === EnhancedMamaBearOrchestrator Integration ===
from .enhanced_mama_bear_orchestrator import EnhancedMamaBearOrchestrator

# For backward compatibility, alias AgentOrchestrator to the enhanced version
AgentOrchestrator = EnhancedMamaBearOrchestrator

class ContextManager:
    """Manages context sharing between agents"""
    def __init__(self):
        self.contexts = {}
        self.shared_state = {}
    async def get_context(self, user_id: str, session_id: str = None) -> Dict[str, Any]:
        key = f"{user_id}:{session_id}" if session_id else user_id
        return self.contexts.get(key, {})
    async def update_context(self, user_id: str, context_update: Dict[str, Any], session_id: str = None):
        key = f"{user_id}:{session_id}" if session_id else user_id
        if key not in self.contexts:
            self.contexts[key] = {}
        self.contexts[key].update(context_update)
    async def share_context(self, from_agent: str, to_agent: str, context_data: Dict[str, Any]):
        share_key = f"{from_agent}:{to_agent}"
        self.shared_state[share_key] = {
            'data': context_data,
            'timestamp': datetime.now().isoformat()
        }

async def initialize_orchestration(memory_manager, model_manager, scrapybara_client):
    orchestrator = AgentOrchestrator(memory_manager, model_manager, scrapybara_client)
    logger.info("🐻 Agent Orchestration System initialized")
    return orchestrator
