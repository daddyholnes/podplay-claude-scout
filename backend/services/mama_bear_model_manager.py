import asyncio
from .gemini_quota_manager import GeminiQuotaManager, QuotaException, ModelType
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json
import os
from dataclasses import dataclass
import logging
from collections import defaultdict
import aiofiles

logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    AVAILABLE = "available"
    QUOTA_EXCEEDED = "quota_exceeded"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class ModelConfig:
    name: str
    api_key: str
    billing_account: int
    priority: int
    rate_limit: int  # requests per minute
    daily_quota: int  # requests per day
    capabilities: List[str]  # ['chat', 'code', 'vision', 'function_calling']

@dataclass
class ModelHealth:
    status: ModelStatus
    last_success: datetime
    error_count: int
    quota_used_today: int
    rate_limit_reset: datetime
    last_error: Optional[str] = None

class MamaBearModelManager:
    """
    Intelligent model management system for Mama Bear that ensures
    continuous service by bouncing between models and API keys.
    Now delegates all Gemini model usage to GeminiQuotaManager.
    """
    def __init__(self, gemini_quota_manager=None):
        self.models = self._initialize_models()
        self.model_health = defaultdict(lambda: ModelHealth(
            status=ModelStatus.AVAILABLE,
            last_success=datetime.now(),
            error_count=0,
            quota_used_today=0,
            rate_limit_reset=datetime.now()
        ))
        self.gemini_quota_manager = gemini_quota_manager or GeminiQuotaManager()
        self.request_history = defaultdict(list)
        asyncio.create_task(self._health_check_loop())

    def _initialize_models(self) -> List[ModelConfig]:
        # This should be customized for your deployment
        # Example: read from config or environment
        return [
            ModelConfig(
                name='gemini-2.5-pro',
                api_key=os.getenv('GEMINI_API_KEY_1', ''),
                billing_account=1,
                priority=1,
                rate_limit=60,
                daily_quota=10000,
                capabilities=['chat', 'code', 'vision', 'function_calling']
            ),
            ModelConfig(
                name='gemini-2.5-flash',
                api_key=os.getenv('GEMINI_API_KEY_2', ''),
                billing_account=2,
                priority=2,
                rate_limit=120,
                daily_quota=20000,
                capabilities=['chat', 'code', 'vision']
            )
        ]

    async def _health_check_loop(self):
        while True:
            for model in self.models:
                health = self.model_health[model.name]
                # Example: check quota, errors, etc.
                if health.error_count > 5:
                    health.status = ModelStatus.ERROR
                if health.quota_used_today > model.daily_quota:
                    health.status = ModelStatus.QUOTA_EXCEEDED
            await asyncio.sleep(60)

    async def chat_with_model(self, model_name: str, prompt: str, **kwargs) -> Any:
        model = next((m for m in self.models if m.name == model_name), None)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        if 'gemini' in model_name:
            try:
                task_type = kwargs.get('task_type', 'chat')
                complexity = kwargs.get('complexity', 'medium')
                return await self.gemini_quota_manager.invoke_model(task_type, prompt, complexity, **kwargs)
            except QuotaException as qe:
                logger.error(f"QuotaException: {qe}")
                raise
        # ... (existing logic for OpenAI, Anthropic, etc.)

    async def get_status(self) -> Dict[str, Any]:
        status = {
            'timestamp': datetime.now().isoformat(),
            'models': []
        }
        for model in self.models:
            health = self.model_health[model.name]
            status['models'].append({
                'name': model.name,
                'billing_account': model.billing_account,
                'status': health.status.value,
                'quota_used': health.quota_used_today,
                'quota_limit': model.daily_quota,
                'error_count': health.error_count,
                'last_success': health.last_success.isoformat(),
                'last_error': health.last_error
            })
        return status
