"""
🐻 Enhanced Mama Bear Memory & Context System
Advanced memory management for persistent agent context and learning
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from collections import defaultdict, deque
import hashlib
import pickle
import os

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    CONVERSATION = "conversation"
    AGENT_CONTEXT = "agent_context"
    USER_PATTERN = "user_pattern"
    DECISION_PATTERN = "decision_pattern"
    COLLABORATION_HISTORY = "collaboration_history"
    LEARNING_INSIGHT = "learning_insight"
    PROJECT_CONTEXT = "project_context"

class MemoryImportance(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1

@dataclass
class MemoryRecord:
    """Represents a single memory record"""
    id: str
    type: MemoryType
    content: Dict[str, Any]
    user_id: str
    agent_id: Optional[str] = None
    importance: MemoryImportance = MemoryImportance.MEDIUM
    tags: List[str] = None
    created_at: datetime = None
    accessed_at: datetime = None
    access_count: int = 0
    related_memories: List[str] = None
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.accessed_at is None:
            self.accessed_at = self.created_at
        if self.related_memories is None:
            self.related_memories = []

@dataclass
class UserProfile:
    """Comprehensive user profile built from interactions"""
    user_id: str
    expertise_level: str = "intermediate"
    preferred_agents: List[str] = None
    communication_style: Dict[str, float] = None
    project_history: List[Dict] = None
    success_patterns: Dict[str, float] = None
    learning_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.preferred_agents is None:
            self.preferred_agents = []
        if self.communication_style is None:
            self.communication_style = {}
        if self.project_history is None:
            self.project_history = []
        if self.success_patterns is None:
            self.success_patterns = {}
        if self.learning_preferences is None:
            self.learning_preferences = {}

class EnhancedMemoryManager:
    """
    Advanced memory manager for persistent agent context, learning, and user profiling.
    Integrates with Mem0 for cloud persistence and supports local fallback.
    """
    def __init__(self, mem0_client=None, local_storage_path="./memory_data"):
        self.mem0_client = mem0_client
        self.local_storage_path = local_storage_path
        self.memory_records = defaultdict(deque)
        self.user_profiles = {}
    
    async def async_init(self):
        await self._load_persistent_data()
    
    async def store_memory(self, content: Dict[str, Any], memory_type: MemoryType, user_id: str, importance: MemoryImportance = MemoryImportance.MEDIUM, agent_id: Optional[str] = None, tags: Optional[List[str]] = None, embedding: Optional[List[float]] = None) -> str:
        memory_id = hashlib.sha256(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
        record = MemoryRecord(
            id=memory_id,
            type=memory_type,
            content=content,
            user_id=user_id,
            agent_id=agent_id,
            importance=importance,
            tags=tags or [],
            embedding=embedding
        )
        self.memory_records[user_id].appendleft(asdict(record))
        await self._save_to_mem0(record)
        await self._save_to_local(record)
        return memory_id
    
    async def retrieve_memories(self, user_id: str, limit: int = 20, memory_type: Optional[MemoryType] = None) -> List[Dict[str, Any]]:
        records = list(self.memory_records[user_id])
        if memory_type:
            records = [r for r in records if r['type'] == memory_type.value]
        return records[:limit]
    
    async def save_interaction(self, user_id: str, message: str, response: str, metadata: Dict[str, Any] = None):
        await self.store_memory(
            content={
                'message': message,
                'response': response,
                'metadata': metadata or {}
            },
            memory_type=MemoryType.CONVERSATION,
            user_id=user_id,
            importance=MemoryImportance.MEDIUM
        )
    
    async def _save_to_local(self, record: MemoryRecord):
        try:
            os.makedirs(self.local_storage_path, exist_ok=True)
            file_path = f"{self.local_storage_path}/{record.user_id}.pkl"
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
            else:
                data = []
            data.insert(0, asdict(record))
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.error(f"Failed to save memory locally: {e}")
    
    async def _load_user_profile(self, user_id: str) -> UserProfile:
        profiles_dir = f"{self.local_storage_path}/profiles"
        os.makedirs(profiles_dir, exist_ok=True)
        file_path = f"{profiles_dir}/{user_id}.pkl"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                profile = pickle.load(f)
            return profile
        else:
            profile = UserProfile(user_id=user_id)
            await self._save_user_profile(profile)
            return profile
    
    async def _save_user_profile(self, profile: UserProfile):
        profiles_dir = f"{self.local_storage_path}/profiles"
        os.makedirs(profiles_dir, exist_ok=True)
        file_path = f"{profiles_dir}/{profile.user_id}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(profile, f)
        self.user_profiles[profile.user_id] = profile
    
    async def update_user_profile(self, user_id: str, **kwargs):
        profile = await self._load_user_profile(user_id)
        for k, v in kwargs.items():
            setattr(profile, k, v)
        await self._save_user_profile(profile)
    
    async def analyze_and_update_user_profile(self, user_id: str):
        # Analyze last 10 memories for user
        recent_memories = list(self.memory_records[user_id])[:10]
        if len(recent_memories) < 3:
            return
        successful_interactions = [m for m in recent_memories if m['content'].get('success', True)]
        failed_interactions = [m for m in recent_memories if not m['content'].get('success', True)]
        profile = await self._load_user_profile(user_id)
        if successful_interactions:
            successful_agents = [m['agent_id'] for m in successful_interactions if m.get('agent_id')]
            for agent in set(successful_agents):
                if agent not in profile.success_patterns:
                    profile.success_patterns[agent] = 0
                profile.success_patterns[agent] += successful_agents.count(agent) / len(successful_interactions)
        await self._save_user_profile(profile)
    
    async def _load_persistent_data(self):
        try:
            profiles_dir = f"{self.local_storage_path}/profiles"
            if os.path.exists(profiles_dir):
                for filename in os.listdir(profiles_dir):
                    if filename.endswith('.pkl'):
                        user_id = filename[:-4]
                        profile = await self._load_user_profile(user_id)
                        self.user_profiles[user_id] = profile
            logger.info(f"Loaded {len(self.user_profiles)} user profiles")
        except Exception as e:
            logger.error(f"Failed to load persistent data: {e}")
    
    async def _save_to_mem0(self, memory_record):
        if not self.mem0_client:
            raise RuntimeError("Mem0 client not initialized")
        try:
            if hasattr(memory_record, '__dict__'):
                data = memory_record.__dict__
            elif hasattr(memory_record, '_asdict'):
                data = memory_record._asdict()
            else:
                data = dict(memory_record)
            await self.mem0_client.save_memory(data)
        except Exception as e:
            logger.error(f"Failed to save memory to Mem0: {e}")

# Integration function
async def initialize_enhanced_memory(mem0_client=None) -> EnhancedMemoryManager:
    memory_manager = EnhancedMemoryManager(mem0_client)
    await memory_manager.async_init()
    logger.info("🧠 Enhanced Mama Bear Memory System initialized!")
    return memory_manager
