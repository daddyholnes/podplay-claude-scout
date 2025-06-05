"""
GeminiQuotaManager: Advanced Gemini 2.5+ Model Quota, Failover, and Service Account Management
Moved from files-research/mama-bear-quota-manager.py for direct backend integration.
"""

import asyncio
import time
import random
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import google.generativeai as genai
from google.oauth2 import service_account
import logging
from abc import ABC, abstractmethod
import os

# Configure logging
logger = logging.getLogger("GeminiQuotaManager")

class ModelType(Enum):
    PRO_PREVIEW_05_06 = "gemini-2.5-pro-preview-05-06"
    FLASH_PREVIEW_04_17 = "gemini-2.5-flash-preview-04-17"
    FLASH_PREVIEW_05_20 = "gemini-2.5-flash-preview-05-20"

@dataclass
class ModelStats:
    total_requests: int = 0
    successful_requests: int = 0
    quota_errors: int = 0
    other_errors: int = 0
    last_quota_error: Optional[datetime] = None
    last_success: Optional[datetime] = None
    average_response_time: float = 0.0
    cooldown_until: Optional[datetime] = None

@dataclass
class BillingAccount:
    id: str
    api_key: Optional[str] = None
    service_account_path: Optional[str] = None
    is_primary: bool = False
    quota_remaining: Optional[int] = None
    reset_time: Optional[datetime] = None
    stats: Dict[ModelType, ModelStats] = field(default_factory=dict)

class QuotaException(Exception):
    pass

class ModelSelector:
    @staticmethod
    def select_model_for_task(task_type: str, complexity: str = "medium") -> List[ModelType]:
        if complexity == "high":
            return [ModelType.PRO_PREVIEW_05_06, ModelType.FLASH_PREVIEW_05_20, ModelType.FLASH_PREVIEW_04_17]
        elif complexity == "low":
            return [ModelType.FLASH_PREVIEW_05_20, ModelType.FLASH_PREVIEW_04_17, ModelType.PRO_PREVIEW_05_06]
        else:
            return [ModelType.FLASH_PREVIEW_04_17, ModelType.FLASH_PREVIEW_05_20, ModelType.PRO_PREVIEW_05_06]

class GeminiQuotaManager:
    def __init__(self):
        self.accounts: List[BillingAccount] = []
        self.model_stats: Dict[ModelType, ModelStats] = {m: ModelStats() for m in ModelType}
        self._load_accounts_from_env()
        self.lock = asyncio.Lock()

    def _load_accounts_from_env(self):
        # Load API keys
        keys = [os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_API_KEY_PRIMARY"), os.getenv("GOOGLE_API_KEY_FALLBACK")]
        for idx, key in enumerate(filter(None, keys)):
            self.accounts.append(BillingAccount(id=f"api_key_{idx}", api_key=key, is_primary=(idx==0)))
        # Load service accounts
        paths = [os.getenv("PRIMARY_SERVICE_ACCOUNT_PATH"), os.getenv("FALLBACK_SERVICE_ACCOUNT_PATH")]
        for idx, path in enumerate(filter(None, paths)):
            self.accounts.append(BillingAccount(id=f"svc_acct_{idx}", service_account_path=path, is_primary=False))

    async def get_account_for_model(self, model: ModelType) -> BillingAccount:
        now = datetime.now()
        # Prefer primary, fallback if quota/cooldown
        for acct in self.accounts:
            stats = acct.stats.setdefault(model, ModelStats())
            if stats.cooldown_until and stats.cooldown_until > now:
                continue
            return acct
        raise QuotaException(f"No available account for model {model}")

    async def record_quota_error(self, account: BillingAccount, model: ModelType):
        stats = account.stats.setdefault(model, ModelStats())
        stats.quota_errors += 1
        stats.last_quota_error = datetime.now()
        # Set cooldown (e.g., 5 min)
        stats.cooldown_until = datetime.now() + timedelta(minutes=5)
        logger.warning(f"Quota error for {account.id} on {model.value}, cooldown until {stats.cooldown_until}")

    async def record_success(self, account: BillingAccount, model: ModelType, response_time: float):
        stats = account.stats.setdefault(model, ModelStats())
        stats.successful_requests += 1
        stats.last_success = datetime.now()
        stats.average_response_time = (
            (stats.average_response_time * (stats.successful_requests - 1) + response_time)
            / stats.successful_requests
        )

    async def invoke_model(self, task_type: str, prompt: str, complexity: str = "medium", **kwargs) -> Any:
        models = ModelSelector.select_model_for_task(task_type, complexity)
        for model in models:
            try:
                acct = await self.get_account_for_model(model)
                start = time.time()
                # Configure credentials
                if acct.api_key:
                    genai.configure(api_key=acct.api_key)
                elif acct.service_account_path:
                    creds = service_account.Credentials.from_service_account_file(acct.service_account_path)
                    genai.configure(credentials=creds)
                else:
                    continue
                # Actually call the model
                response = genai.GenerativeModel(model.value).generate_content(prompt, **kwargs)
                elapsed = time.time() - start
                await self.record_success(acct, model, elapsed)
                return response
            except Exception as e:
                logger.error(f"Error invoking {model.value} with {acct.id}: {e}")
                if "quota" in str(e).lower():
                    await self.record_quota_error(acct, model)
                    continue
                else:
                    raise
        raise QuotaException("All models/accounts exhausted or failed.")
