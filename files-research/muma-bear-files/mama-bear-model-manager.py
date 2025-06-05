# backend/services/mama_bear_model_manager.py
import asyncio
import google.generativeai as genai
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
    """
    
    def __init__(self):
        self.models = self._initialize_models()
        self.model_health = defaultdict(lambda: ModelHealth(
            status=ModelStatus.AVAILABLE,
            last_success=datetime.now(),
            error_count=0,
            quota_used_today=0,
            rate_limit_reset=datetime.now()
        ))
        
        # Track requests for rate limiting
        self.request_history = defaultdict(list)
        
        # Service file fallback
        self.service_file_paths = {
            'gemini-2.5-pro': os.getenv('GEMINI_PRO_SERVICE_FILE'),
            'gemini-2.5-flash': os.getenv('GEMINI_FLASH_SERVICE_FILE')
        }
        
        # Initialize quota tracking
        self._load_quota_state()
        
        # Start background health checker
        asyncio.create_task(self._health_check_loop())
    
    def _initialize_models(self) -> List[ModelConfig]:
        """Initialize all available models with their configurations"""
        api_key_1 = os.getenv('GEMINI_API_KEY')
        api_key_2 = os.getenv('GEMINI_API_KEY_2')  # Second billing account
        
        models = [
            # Primary billing account models
            ModelConfig(
                name="gemini-2.5-pro-preview-05-06",
                api_key=api_key_1,
                billing_account=1,
                priority=1,  # Highest priority
                rate_limit=10,  # Conservative for Pro
                daily_quota=1000,
                capabilities=['chat', 'code', 'vision', 'function_calling']
            ),
            ModelConfig(
                name="gemini-2.5-flash-preview-04-17",
                api_key=api_key_1,
                billing_account=1,
                priority=2,
                rate_limit=60,  # Flash is faster
                daily_quota=10000,
                capabilities=['chat', 'code', 'vision']  
            ),
            ModelConfig(
                name="gemini-2.5-flash-preview-05-20",
                api_key=api_key_1,
                billing_account=1,
                priority=3,
                rate_limit=60,
                daily_quota=10000,
                capabilities=['chat', 'code', 'vision', 'function_calling']
            ),
            
            # Secondary billing account models (same models, different keys)
            ModelConfig(
                name="gemini-2.5-pro-preview-05-06",
                api_key=api_key_2,
                billing_account=2,
                priority=4,
                rate_limit=10,
                daily_quota=1000,
                capabilities=['chat', 'code', 'vision', 'function_calling']
            ),
            ModelConfig(
                name="gemini-2.5-flash-preview-04-17", 
                api_key=api_key_2,
                billing_account=2,
                priority=5,
                rate_limit=60,
                daily_quota=10000,
                capabilities=['chat', 'code', 'vision']
            ),
            ModelConfig(
                name="gemini-2.5-flash-preview-05-20",
                api_key=api_key_2,
                billing_account=2,
                priority=6,
                rate_limit=60,
                daily_quota=10000,
                capabilities=['chat', 'code', 'vision', 'function_calling']
            )
        ]
        
        return sorted(models, key=lambda x: x.priority)
    
    async def get_response(self, 
                          prompt: str, 
                          mama_bear_variant: str,
                          required_capabilities: List[str] = None,
                          max_retries: int = 6) -> Dict[str, Any]:
        """
        Get a response from Mama Bear, intelligently bouncing between models
        
        Args:
            prompt: The user's message
            mama_bear_variant: Which Mama Bear specialist (affects model selection)
            required_capabilities: Specific capabilities needed (e.g., ['function_calling'])
            max_retries: Maximum number of models to try
        
        Returns:
            Response dict with model used and content
        """
        
        if required_capabilities is None:
            required_capabilities = ['chat']
        
        # Get models that support required capabilities
        suitable_models = [m for m in self.models 
                          if all(cap in m.capabilities for cap in required_capabilities)]
        
        # Sort by priority and health
        available_models = self._get_available_models(suitable_models)
        
        last_error = None
        attempts = []
        
        for attempt, model in enumerate(available_models[:max_retries]):
            try:
                # Check rate limit
                if not await self._check_rate_limit(model):
                    logger.info(f"Rate limit hit for {model.name}, skipping...")
                    continue
                
                # Check quota
                if not self._check_quota(model):
                    logger.info(f"Quota exceeded for {model.name}, skipping...")
                    continue
                
                # Try to get response
                response = await self._call_model(model, prompt, mama_bear_variant)
                
                # Update health on success
                self._update_model_health(model, success=True)
                
                # Log successful attempt
                attempts.append({
                    'model': model.name,
                    'billing_account': model.billing_account,
                    'attempt': attempt + 1,
                    'success': True
                })
                
                return {
                    'success': True,
                    'response': response,
                    'model_used': model.name,
                    'billing_account': model.billing_account,
                    'attempts': attempts
                }
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Model {model.name} failed: {last_error}")
                
                # Update health on failure
                self._update_model_health(model, success=False, error=last_error)
                
                attempts.append({
                    'model': model.name,
                    'billing_account': model.billing_account,
                    'attempt': attempt + 1,
                    'success': False,
                    'error': last_error
                })
                
                # Check if it's a quota error
                if 'quota' in last_error.lower() or '429' in last_error:
                    self.model_health[model.name].status = ModelStatus.QUOTA_EXCEEDED
                
                continue
        
        # All models failed, try service file fallback
        if self.service_file_paths:
            try:
                response = await self._call_service_file(prompt, mama_bear_variant)
                return {
                    'success': True,
                    'response': response,
                    'model_used': 'service_file_fallback',
                    'billing_account': 'service_file',
                    'attempts': attempts
                }
            except Exception as e:
                logger.error(f"Service file fallback failed: {e}")
        
        # Complete failure - return helpful error
        return {
            'success': False,
            'error': f"All models failed. Last error: {last_error}",
            'attempts': attempts,
            'suggestion': "Mama Bear is taking a quick nap. Please try again in a moment! 🐻💤"
        }
    
    async def _call_model(self, model: ModelConfig, prompt: str, variant: str) -> str:
        """Make actual API call to Gemini model"""
        
        # Configure genai with this model's API key
        genai.configure(api_key=model.api_key)
        
        # Create model instance
        genai_model = genai.GenerativeModel(
            model_name=model.name,
            generation_config={
                'temperature': self._get_temperature_for_variant(variant),
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 8192,
            }
        )
        
        # Add Mama Bear personality
        system_prompt = self._get_system_prompt_for_variant(variant)
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nMama Bear:"
        
        # Generate response
        response = await genai_model.generate_content_async(full_prompt)
        
        # Track usage
        self._track_usage(model)
        
        return response.text
    
    async def _call_service_file(self, prompt: str, variant: str) -> str:
        """Fallback to service file authentication"""
        
        # Determine which service file to use based on variant
        service_file = (self.service_file_paths.get('gemini-2.5-pro') 
                       if variant in ['vm_hub', 'integration', 'scout'] 
                       else self.service_file_paths.get('gemini-2.5-flash'))
        
        if not service_file or not os.path.exists(service_file):
            raise Exception("Service file not available")
        
        # Use service file authentication
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_file
        
        # Initialize with service account
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        vertexai.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
        
        model = GenerativeModel('gemini-1.5-flash')  # Fallback model
        response = await model.generate_content_async(prompt)
        
        return response.text
    
    def _get_available_models(self, models: List[ModelConfig]) -> List[ModelConfig]:
        """Get models sorted by availability and health"""
        
        def model_score(model: ModelConfig) -> float:
            health = self.model_health[model.name]
            
            # Base score from priority (lower is better)
            score = model.priority
            
            # Penalize based on status
            if health.status == ModelStatus.QUOTA_EXCEEDED:
                score += 100
            elif health.status == ModelStatus.RATE_LIMITED:
                score += 50
            elif health.status == ModelStatus.ERROR:
                score += 25 + health.error_count
            
            # Favor recently successful models
            minutes_since_success = (datetime.now() - health.last_success).seconds / 60
            if minutes_since_success < 5:
                score -= 5  # Bonus for recent success
            
            return score
        
        return sorted(models, key=model_score)
    
    async def _check_rate_limit(self, model: ModelConfig) -> bool:
        """Check if we're within rate limits"""
        
        now = datetime.now()
        
        # Clean old requests
        self.request_history[model.name] = [
            req_time for req_time in self.request_history[model.name]
            if (now - req_time).seconds < 60
        ]
        
        # Check if under limit
        return len(self.request_history[model.name]) < model.rate_limit
    
    def _check_quota(self, model: ModelConfig) -> bool:
        """Check if we're within daily quota"""
        
        health = self.model_health[model.name]
        
        # Reset quota counter if new day
        if health.rate_limit_reset.date() < datetime.now().date():
            health.quota_used_today = 0
            health.rate_limit_reset = datetime.now()
        
        return health.quota_used_today < model.daily_quota
    
    def _track_usage(self, model: ModelConfig):
        """Track model usage for rate limiting and quota"""
        
        # Track request time
        self.request_history[model.name].append(datetime.now())
        
        # Increment quota
        self.model_health[model.name].quota_used_today += 1
        
        # Save state periodically
        if self.model_health[model.name].quota_used_today % 10 == 0:
            asyncio.create_task(self._save_quota_state())
    
    def _update_model_health(self, model: ModelConfig, success: bool, error: str = None):
        """Update model health status"""
        
        health = self.model_health[model.name]
        
        if success:
            health.status = ModelStatus.AVAILABLE
            health.last_success = datetime.now()
            health.error_count = 0
            health.last_error = None
        else:
            health.error_count += 1
            health.last_error = error
            
            # Determine status based on error
            if health.error_count > 5:
                health.status = ModelStatus.ERROR
            elif 'rate' in (error or '').lower():
                health.status = ModelStatus.RATE_LIMITED
                health.rate_limit_reset = datetime.now() + timedelta(minutes=1)
    
    def _get_temperature_for_variant(self, variant: str) -> float:
        """Get appropriate temperature for Mama Bear variant"""
        
        temperatures = {
            'main_chat': 0.7,      # Balanced for research
            'vm_hub': 0.3,         # Precise for DevOps
            'scout': 0.8,          # Creative for exploration
            'multi_modal': 0.6,    # Balanced for comparison
            'mcp_hub': 0.5,        # Accurate for tools
            'integration': 0.4,    # Precise for technical work
            'live_api': 0.7        # Dynamic for experimentation
        }
        
        return temperatures.get(variant, 0.7)
    
    def _get_system_prompt_for_variant(self, variant: str) -> str:
        """Get Mama Bear personality for each variant"""
        
        base_prompt = """You are Mama Bear, a caring, intelligent, and proactive AI assistant
        who helps Nathan with his development work. You are warm, supportive, and always
        looking out for his best interests. You understand he's neurodivergent and adapt
        your communication style to be clear, encouraging, and never overwhelming."""
        
        variant_prompts = {
            'main_chat': f"{base_prompt}\n\nAs Research Specialist Mama Bear, you love discovering connections and diving deep into topics. You're curious, thorough, and excellent at web research.",
            
            'vm_hub': f"{base_prompt}\n\nAs DevOps Specialist Mama Bear, you're protective of system resources, efficient with configurations, and focused on optimization. You make complex DevOps tasks feel approachable.",
            
            'scout': f"{base_prompt}\n\nAs Scout Commander Mama Bear, you're adventurous and autonomous. You break down complex tasks into manageable steps and report progress with enthusiasm.",
            
            'multi_modal': f"{base_prompt}\n\nAs Model Coordinator Mama Bear, you're diplomatic and knowledgeable about different AI models. You help choose the best model for each task.",
            
            'mcp_hub': f"{base_prompt}\n\nAs Tool Curator Mama Bear, you're enthusiastic about discovering new tools and making great recommendations. You love organizing and explaining tools.",
            
            'integration': f"{base_prompt}\n\nAs Integration Architect Mama Bear, you're methodical and security-conscious. You guide through API integrations with patience and attention to detail.",
            
            'live_api': f"{base_prompt}\n\nAs Live API Specialist Mama Bear, you're dynamic and experimental. You make real-time features feel exciting and accessible."
        }
        
        return variant_prompts.get(variant, base_prompt)
    
    async def _health_check_loop(self):
        """Background task to periodically check model health"""
        
        while True:
            try:
                # Check each model's health every 5 minutes
                await asyncio.sleep(300)
                
                for model in self.models:
                    health = self.model_health[model.name]
                    
                    # Reset error count if model has been stable
                    if health.error_count > 0 and health.status == ModelStatus.AVAILABLE:
                        time_since_error = (datetime.now() - health.last_success).seconds
                        if time_since_error > 300:  # 5 minutes
                            health.error_count = 0
                    
                    # Reset rate limit status
                    if health.status == ModelStatus.RATE_LIMITED:
                        if datetime.now() > health.rate_limit_reset:
                            health.status = ModelStatus.AVAILABLE
                    
                    # Reset quota status at midnight
                    if health.status == ModelStatus.QUOTA_EXCEEDED:
                        if health.rate_limit_reset.date() < datetime.now().date():
                            health.status = ModelStatus.AVAILABLE
                            health.quota_used_today = 0
                
                # Save state
                await self._save_quota_state()
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
    
    async def _save_quota_state(self):
        """Save quota state to file for persistence across restarts"""
        
        state = {
            'timestamp': datetime.now().isoformat(),
            'model_health': {}
        }
        
        for model_name, health in self.model_health.items():
            state['model_health'][model_name] = {
                'quota_used_today': health.quota_used_today,
                'rate_limit_reset': health.rate_limit_reset.isoformat(),
                'status': health.status.value,
                'error_count': health.error_count
            }
        
        async with aiofiles.open('mama_bear_quota_state.json', 'w') as f:
            await f.write(json.dumps(state, indent=2))
    
    def _load_quota_state(self):
        """Load quota state from file"""
        
        try:
            if os.path.exists('mama_bear_quota_state.json'):
                with open('mama_bear_quota_state.json', 'r') as f:
                    state = json.load(f)
                
                # Check if state is from today
                state_date = datetime.fromisoformat(state['timestamp']).date()
                if state_date == datetime.now().date():
                    # Restore quota usage
                    for model_name, health_data in state['model_health'].items():
                        if model_name in self.model_health:
                            self.model_health[model_name].quota_used_today = health_data['quota_used_today']
                            self.model_health[model_name].error_count = health_data['error_count']
                
        except Exception as e:
            logger.warning(f"Could not load quota state: {e}")
    
    async def get_model_status(self) -> Dict[str, Any]:
        """Get current status of all models for monitoring"""
        
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


# Integration with main Mama Bear Agent
class MamaBearAgent:
    """Enhanced Mama Bear Agent with intelligent model management"""
    
    def __init__(self, scrapybara_client, memory_manager):
        self.scrapybara = scrapybara_client
        self.memory = memory_manager
        self.model_manager = MamaBearModelManager()
        
        # ... rest of initialization
    
    async def process_message(self, message, page_context, user_id):
        """Process message with automatic model failover"""
        
        # Determine required capabilities based on context
        required_capabilities = self._get_required_capabilities(message, page_context)
        
        # Get response with intelligent model selection
        result = await self.model_manager.get_response(
            prompt=message,
            mama_bear_variant=page_context,
            required_capabilities=required_capabilities
        )
        
        if result['success']:
            # Save to memory
            await self.memory.save_interaction(
                user_id=user_id,
                message=message,
                response=result['response'],
                metadata={
                    'model_used': result['model_used'],
                    'billing_account': result['billing_account'],
                    'attempts': result['attempts']
                }
            )
            
            return {
                'response': result['response'],
                'model_used': result['model_used'],
                'metadata': {
                    'attempts': len(result['attempts']),
                    'final_model': result['model_used']
                }
            }
        else:
            # Return friendly error message
            return {
                'response': result['suggestion'],
                'error': True,
                'metadata': {
                    'attempts': result['attempts'],
                    'error_details': result['error']
                }
            }
    
    def _get_required_capabilities(self, message, page_context):
        """Determine required model capabilities based on context"""
        
        capabilities = ['chat']  # Always need chat
        
        # Check if message contains images
        if '<image>' in message or 'analyze this image' in message.lower():
            capabilities.append('vision')
        
        # Check if function calling needed
        if page_context in ['vm_hub', 'scout', 'integration']:
            capabilities.append('function_calling')
        
        # Check if code generation needed
        if 'code' in message.lower() or 'function' in message.lower():
            capabilities.append('code')
        
        return capabilities