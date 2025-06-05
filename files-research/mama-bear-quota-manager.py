"""
🐻 Mama Bear Intelligent Quota Management System
Handles multiple Gemini 2.5 models with automatic failover and quota management
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MamaBear")

class ModelType(Enum):
    """Available Gemini 2.5 models"""
    PRO_PREVIEW_05_06 = "gemini-2.5-pro-preview-05-06"
    FLASH_PREVIEW_04_17 = "gemini-2.5-flash-preview-04-17"
    FLASH_PREVIEW_05_20 = "gemini-2.5-flash-preview-05-20"

@dataclass
class ModelStats:
    """Track model performance and quota usage"""
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
    """Represents a billing account with API key or service account"""
    id: str
    api_key: Optional[str] = None
    service_account_path: Optional[str] = None
    is_primary: bool = False
    quota_remaining: Optional[int] = None
    reset_time: Optional[datetime] = None
    stats: Dict[ModelType, ModelStats] = field(default_factory=dict)

class QuotaException(Exception):
    """Raised when quota limit is reached"""
    pass

class ModelSelector:
    """Intelligent model selection based on task requirements"""
    
    @staticmethod
    def select_model_for_task(task_type: str, complexity: str = "medium") -> List[ModelType]:
        """
        Returns ordered list of models best suited for the task
        
        Pro: Best for complex reasoning, code generation, detailed analysis
        Flash: Best for quick responses, simple tasks, high-volume operations
        """
        if task_type in ["code_generation", "complex_analysis", "architecture_design"]:
            return [
                ModelType.PRO_PREVIEW_05_06,
                ModelType.FLASH_PREVIEW_05_20,
                ModelType.FLASH_PREVIEW_04_17
            ]
        elif task_type in ["quick_response", "simple_query", "status_check"]:
            return [
                ModelType.FLASH_PREVIEW_05_20,
                ModelType.FLASH_PREVIEW_04_17,
                ModelType.PRO_PREVIEW_05_06
            ]
        else:  # Default balanced approach
            return [
                ModelType.FLASH_PREVIEW_05_20,
                ModelType.PRO_PREVIEW_05_06,
                ModelType.FLASH_PREVIEW_04_17
            ]

class MamaBearQuotaManager:
    """
    🐻 Intelligent quota management for Mama Bear
    Handles multiple models, billing accounts, and automatic failover
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.accounts: List[BillingAccount] = []
        self.current_account_index = 0
        self.model_stats: Dict[str, Dict[ModelType, ModelStats]] = {}
        self.config = config
        self._setup_accounts()
        
    def _setup_accounts(self):
        """Initialize billing accounts from config"""
        for acc_config in self.config['billing_accounts']:
            account = BillingAccount(
                id=acc_config['id'],
                api_key=acc_config.get('api_key'),
                service_account_path=acc_config.get('service_account_path'),
                is_primary=acc_config.get('is_primary', False)
            )
            
            # Initialize stats for each model
            for model_type in ModelType:
                account.stats[model_type] = ModelStats()
                
            self.accounts.append(account)
            
        # Sort so primary account is first
        self.accounts.sort(key=lambda x: x.is_primary, reverse=True)
    
    def _get_client(self, account: BillingAccount):
        """Get appropriate Gemini client for the account"""
        if account.api_key:
            genai.configure(api_key=account.api_key)
        elif account.service_account_path:
            # Use service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                account.service_account_path
            )
            genai.configure(credentials=credentials)
        else:
            raise ValueError(f"No credentials found for account {account.id}")
    
    async def _try_model_with_account(
        self, 
        model_type: ModelType, 
        account: BillingAccount,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[str]:
        """Try to get response from specific model with specific account"""
        
        # Check if model is in cooldown
        stats = account.stats[model_type]
        if stats.cooldown_until and datetime.now() < stats.cooldown_until:
            logger.info(f"Model {model_type.value} on account {account.id} is in cooldown")
            return None
        
        try:
            start_time = time.time()
            
            # Configure client for this account
            self._get_client(account)
            
            # Initialize model
            model = genai.GenerativeModel(
                model_name=model_type.value,
                system_instruction=system_prompt
            )
            
            # Generate response
            response = await model.generate_content_async(prompt, **kwargs)
            
            # Update success stats
            elapsed = time.time() - start_time
            stats.total_requests += 1
            stats.successful_requests += 1
            stats.last_success = datetime.now()
            stats.average_response_time = (
                (stats.average_response_time * (stats.successful_requests - 1) + elapsed) 
                / stats.successful_requests
            )
            
            logger.info(
                f"✅ Success with {model_type.value} on account {account.id} "
                f"(Response time: {elapsed:.2f}s)"
            )
            
            return response.text
            
        except Exception as e:
            stats.total_requests += 1
            
            if "quota" in str(e).lower() or "rate limit" in str(e).lower():
                stats.quota_errors += 1
                stats.last_quota_error = datetime.now()
                
                # Implement exponential backoff cooldown
                cooldown_minutes = min(60, 5 * (2 ** min(stats.quota_errors, 5)))
                stats.cooldown_until = datetime.now() + timedelta(minutes=cooldown_minutes)
                
                logger.warning(
                    f"⚠️ Quota error for {model_type.value} on account {account.id}. "
                    f"Cooldown for {cooldown_minutes} minutes"
                )
                
                raise QuotaException(f"Quota exceeded for {model_type.value}")
            else:
                stats.other_errors += 1
                logger.error(f"❌ Error with {model_type.value}: {str(e)}")
                raise
    
    async def get_response(
        self,
        prompt: str,
        task_type: str = "general",
        complexity: str = "medium",
        system_prompt: Optional[str] = None,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        🐻 Intelligently get response from available models and accounts
        
        Returns dict with:
        - response: The generated text
        - model_used: Which model provided the response
        - account_used: Which account was used
        - attempts: Number of attempts made
        """
        
        # Get ordered list of models for this task
        model_priority = ModelSelector.select_model_for_task(task_type, complexity)
        
        attempts = 0
        errors = []
        
        # Try each model in priority order
        for model_type in model_priority:
            # Try each account (primary first)
            for account in self.accounts:
                attempts += 1
                
                try:
                    response = await self._try_model_with_account(
                        model_type=model_type,
                        account=account,
                        prompt=prompt,
                        system_prompt=system_prompt,
                        **kwargs
                    )
                    
                    if response:
                        return {
                            "response": response,
                            "model_used": model_type.value,
                            "account_used": account.id,
                            "attempts": attempts,
                            "success": True
                        }
                        
                except QuotaException as e:
                    errors.append(str(e))
                    # Continue to next account/model
                    continue
                    
                except Exception as e:
                    errors.append(f"{model_type.value} on {account.id}: {str(e)}")
                    
                    # For non-quota errors, retry with small delay
                    if attempts < max_retries:
                        await asyncio.sleep(1)
                        continue
        
        # All attempts failed
        logger.error(f"🚨 All models failed after {attempts} attempts")
        return {
            "response": None,
            "model_used": None,
            "account_used": None,
            "attempts": attempts,
            "success": False,
            "errors": errors
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status of all models and accounts"""
        status = {
            "accounts": {},
            "models": {},
            "overall_health": "healthy"
        }
        
        total_available = 0
        
        for account in self.accounts:
            account_health = {
                "id": account.id,
                "models": {}
            }
            
            for model_type, stats in account.stats.items():
                model_health = {
                    "available": stats.cooldown_until is None or datetime.now() > stats.cooldown_until,
                    "success_rate": (
                        stats.successful_requests / stats.total_requests 
                        if stats.total_requests > 0 else 1.0
                    ),
                    "quota_errors": stats.quota_errors,
                    "avg_response_time": stats.average_response_time
                }
                
                account_health["models"][model_type.value] = model_health
                if model_health["available"]:
                    total_available += 1
            
            status["accounts"][account.id] = account_health
        
        # Determine overall health
        if total_available == 0:
            status["overall_health"] = "critical"
        elif total_available < len(self.accounts) * len(ModelType) * 0.5:
            status["overall_health"] = "degraded"
        
        return status

# Enhanced Mama Bear Agent with Quota Management
class MamaBearAgent:
    """
    🐻 Enhanced Mama Bear with intelligent quota management
    Integrates with Scrapybara for full desktop control
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.quota_manager = MamaBearQuotaManager(config)
        self.scrapybara = self._init_scrapybara()
        
    def _init_scrapybara(self):
        """Initialize Scrapybara if available"""
        try:
            from scrapybara import Scrapybara
            return Scrapybara()
        except ImportError:
            logger.warning("Scrapybara not available - desktop features disabled")
            return None
    
    async def think(
        self, 
        prompt: str, 
        context: Optional[Dict] = None,
        task_type: str = "general"
    ) -> str:
        """
        🐻 Mama Bear thinks about your request using best available model
        """
        
        # Build system prompt with context
        system_prompt = self._build_system_prompt(context)
        
        # Get response with intelligent failover
        result = await self.quota_manager.get_response(
            prompt=prompt,
            task_type=task_type,
            system_prompt=system_prompt,
            temperature=0.7,
            max_output_tokens=4096
        )
        
        if result["success"]:
            logger.info(
                f"🐻 Mama Bear responded using {result['model_used']} "
                f"(Account: {result['account_used']}, Attempts: {result['attempts']})"
            )
            return result["response"]
        else:
            # Fallback response when all models fail
            return self._get_fallback_response(prompt, result["errors"])
    
    def _build_system_prompt(self, context: Optional[Dict]) -> str:
        """Build contextual system prompt for Mama Bear"""
        base_prompt = """
        🐻 You are Mama Bear, a caring, intelligent AI assistant.
        You are proactive, globally capable, and always learning.
        You help create perfect development environments and guide users with wisdom and care.
        """
        
        if context:
            base_prompt += f"\n\nCurrent context: {context}"
            
        return base_prompt
    
    def _get_fallback_response(self, prompt: str, errors: List[str]) -> str:
        """Generate helpful fallback when all models fail"""
        return f"""
        🐻 Oh dear, I'm having some technical difficulties right now.
        
        All my AI models are currently experiencing quota limits or errors.
        Here's what I tried:
        {chr(10).join(f"- {error}" for error in errors[:3])}
        
        Don't worry though! I'll be back soon. In the meantime:
        1. The quota limits usually reset within an hour
        2. You can check my health status with mama_bear.get_health_status()
        3. I'm saving your request and will prioritize it when I'm back
        
        Your request: "{prompt[:100]}..."
        
        ☕ Take a break, and I'll be ready to help again soon!
        """

# Example configuration
MAMA_BEAR_CONFIG = {
    "billing_accounts": [
        {
            "id": "primary_account",
            "api_key": "YOUR_PRIMARY_API_KEY",  # First API key
            "is_primary": True
        },
        {
            "id": "secondary_account", 
            "api_key": "YOUR_SECONDARY_API_KEY",  # Second API key
            "is_primary": False
        },
        {
            "id": "service_account",
            "service_account_path": "/path/to/service-account.json",  # Service account
            "is_primary": False
        }
    ],
    "quota_settings": {
        "cooldown_base_minutes": 5,
        "max_cooldown_minutes": 60,
        "retry_delays": [1, 2, 5, 10]
    }
}

# Usage Example
async def main():
    """Example usage of Mama Bear with quota management"""
    
    # Initialize Mama Bear
    mama_bear = MamaBearAgent(MAMA_BEAR_CONFIG)
    
    # Simple query - will use Flash model first
    response = await mama_bear.think(
        "What's the weather like?",
        task_type="simple_query"
    )
    print(response)
    
    # Complex task - will use Pro model first
    response = await mama_bear.think(
        "Design a microservices architecture for a social media platform",
        task_type="architecture_design"
    )
    print(response)
    
    # Check health status
    health = mama_bear.quota_manager.get_health_status()
    print(f"Health Status: {health['overall_health']}")

if __name__ == "__main__":
    asyncio.run(main())
