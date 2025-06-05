"""
🐻 Mama Bear Agent - The caring, intelligent AI system for Podplay Sanctuary
Enhanced with quota management and specialized variants
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os

from .mama_bear_model_manager import MamaBearModelManager
from .mama_bear_variants import *
from .memory_manager import MemoryManager
from .scrapybara_manager import ScrapybaraManager

logger = logging.getLogger(__name__)

class MamaBearAgent:
    """Main Mama Bear agent with specialized variants and intelligent capabilities"""
    
    def __init__(self, scrapybara_manager: ScrapybaraManager, memory_manager: MemoryManager):
        self.scrapybara = scrapybara_manager
        self.memory = memory_manager
        self.model_manager = MamaBearModelManager()
        
        # Initialize specialized variants
        self.variants = {
            'main_chat': ResearchSpecialist(),
            'vm_hub': DevOpsSpecialist(),
            'scout': ScoutCommander(),
            'multi_modal': ModelCoordinator(),
            'mcp_hub': ToolCurator(),
            'integration': IntegrationArchitect(),
            'live_api': LiveAPISpecialist()
        }
        
        logger.info("🐻 Mama Bear Agent initialized with all variants")
    
    async def process_message(self, 
                            message: str, 
                            page_context: str, 
                            user_id: str,
                            attachments: List[Any] = None) -> Dict[str, Any]:
        """Process a message with the appropriate Mama Bear variant"""
        
        try:
            # Get the appropriate variant
            variant = self.variants.get(page_context, self.variants['main_chat'])
            
            # Load conversation memory
            context = await self.memory.get_context(user_id, page_context)
            
            # Determine required capabilities
            required_capabilities = self._get_required_capabilities(message, page_context, attachments)
            
            # Build enhanced prompt with variant personality
            enhanced_prompt = self._build_enhanced_prompt(message, variant, context, attachments)
            
            # Get response with intelligent model selection
            result = await self.model_manager.get_response(
                prompt=enhanced_prompt,
                mama_bear_variant=page_context,
                required_capabilities=required_capabilities
            )
            
            if result['success']:
                # Save interaction to memory
                await self.memory.save_interaction(
                    user_id=user_id,
                    page_context=page_context,
                    message=message,
                    response=result['response'],
                    metadata={
                        'model_used': result['model_used'],
                        'billing_account': result.get('billing_account'),
                        'attempts': result.get('attempts', []),
                        'variant': page_context
                    }
                )
                
                return {
                    'content': result['response'],
                    'metadata': {
                        'model_used': result['model_used'],
                        'variant': variant.__class__.__name__,
                        'attempts': len(result.get('attempts', [])),
                        'processing_time': result.get('processing_time', 0)
                    }
                }
            else:
                # Return friendly fallback response
                fallback_response = self._get_fallback_response(variant, result.get('error', ''))
                
                return {
                    'content': fallback_response,
                    'metadata': {
                        'error': True,
                        'fallback': True,
                        'variant': variant.__class__.__name__,
                        'attempts': result.get('attempts', [])
                    }
                }
                
        except Exception as e:
            logger.error(f"Message processing error: {e}")
            
            # Return caring error message
            return {
                'content': f"🐻 I'm having a small hiccup right now. Let me take a deep breath and try again! (Error: {str(e)})",
                'metadata': {
                    'error': True,
                    'exception': str(e)
                }
            }
    
    def _get_required_capabilities(self, message: str, page_context: str, attachments: List[Any] = None) -> List[str]:
        """Determine required model capabilities based on context"""
        
        capabilities = ['chat']  # Always need chat
        
        # Check for image/visual needs
        if attachments and any('image' in str(att).lower() for att in attachments):
            capabilities.append('vision')
        
        if 'image' in message.lower() or 'picture' in message.lower() or 'visual' in message.lower():
            capabilities.append('vision')
        
        # Check for function calling needs (Scrapybara integration)
        if page_context in ['vm_hub', 'scout', 'integration', 'live_api']:
            capabilities.append('function_calling')
        
        # Check for code generation needs
        code_keywords = ['code', 'function', 'script', 'program', 'algorithm', 'implement']
        if any(keyword in message.lower() for keyword in code_keywords):
            capabilities.append('code')
        
        return capabilities
    
    def _build_enhanced_prompt(self, message: str, variant: Any, context: Dict, attachments: List[Any] = None) -> str:
        """Build enhanced prompt with Mama Bear personality and context"""
        
        # Get variant's system prompt
        system_prompt = variant.get_system_prompt()
        
        # Add context if available
        context_str = ""
        if context and context.get('recent_interactions'):
            context_str = f"\n\nRecent conversation context:\n{context['recent_interactions']}"
        
        # Add attachment context
        attachment_str = ""
        if attachments:
            attachment_str = f"\n\nUser has shared {len(attachments)} attachment(s) with this message."
        
        # Build full prompt
        full_prompt = f"""{system_prompt}

{context_str}{attachment_str}

Current user message: {message}

Remember to respond as Mama Bear - caring, intelligent, and always helpful. Keep your response warm and encouraging while being incredibly useful."""
        
        return full_prompt
    
    def _get_fallback_response(self, variant: Any, error: str) -> str:
        """Get a caring fallback response when all models fail"""
        
        variant_fallbacks = {
            'ResearchSpecialist': "🐻 I'm having trouble with my research tools right now, but I'm still here to help! Could you try rephrasing your question, or would you like me to try again in a moment?",
            'DevOpsSpecialist': "🐻 My DevOps systems are taking a little break, but I haven't forgotten about your infrastructure needs! Let me regroup and we can tackle this together.",
            'ScoutCommander': "🐻 My autonomous systems are recharging, but the spirit of exploration is still strong! I'm ready to plan our next adventure while my tools come back online.",
            'ModelCoordinator': "🐻 I'm having some coordination challenges with my AI models right now, but I can still offer guidance! What would you like to explore?",
            'ToolCurator': "🐻 My tool discovery system is taking a coffee break, but I love talking about great tools! Tell me what you're trying to accomplish.",
            'IntegrationArchitect': "🐻 My integration tools are updating, but I'm still here to help plan your connections! What systems are you looking to integrate?",
            'LiveAPISpecialist': "🐻 My real-time systems are in a brief timeout, but I'm excited to discuss your live API needs! What kind of real-time magic are you creating?"
        }
        
        variant_name = variant.__class__.__name__
        fallback = variant_fallbacks.get(variant_name, 
            "🐻 I'm having a small technical hiccup, but I'm still here for you! Let's try again in just a moment. ✨")
        
        return fallback
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        try:
            # Get model manager status
            model_status = await self.model_manager.get_model_status()
            
            # Get memory status
            memory_status = await self.memory.get_status()
            
            # Get Scrapybara status
            scrapybara_status = await self.scrapybara.get_status()
            
            # Calculate overall health
            model_health = model_status.get('overall_health', 'unknown')
            memory_health = 'healthy' if memory_status.get('connected', False) else 'error'
            scrapybara_health = 'healthy' if scrapybara_status.get('available', False) else 'degraded'
            
            # Determine overall health
            health_scores = {
                'healthy': 3,
                'degraded': 2,
                'critical': 1,
                'error': 0,
                'unknown': 1
            }
            
            min_score = min([
                health_scores.get(model_health, 1),
                health_scores.get(memory_health, 1),
                health_scores.get(scrapybara_health, 1)
            ])
            
            overall_health = {v: k for k, v in health_scores.items()}[min_score]
            
            return {
                'overall_health': overall_health,
                'mama_bear_status': 'active',
                'variants_available': list(self.variants.keys()),
                'services': {
                    'model_manager': model_status,
                    'memory': memory_status,
                    'scrapybara': scrapybara_status
                },
                'capabilities': {
                    'chat': True,
                    'vision': model_health in ['healthy', 'degraded'],
                    'function_calling': scrapybara_health in ['healthy', 'degraded'],
                    'code_generation': model_health in ['healthy', 'degraded'],
                    'autonomous_tasks': scrapybara_health == 'healthy'
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {
                'overall_health': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def execute_autonomous_task(self, 
                                   task_description: str, 
                                   user_id: str,
                                   progress_callback=None) -> Dict[str, Any]:
        """Execute autonomous task using Scout Commander variant"""
        
        try:
            scout_variant = self.variants['scout']
            
            # Build task planning prompt
            planning_prompt = f"""{scout_variant.get_system_prompt()}

I need to execute this autonomous task:
{task_description}

Please break this down into clear steps and execute it systematically. Report your progress as you go.

Remember: I'm Scout Commander Mama Bear - adventurous, strategic, and autonomous while keeping humans informed!"""
            
            # Get response for task planning
            plan_result = await self.model_manager.get_response(
                prompt=planning_prompt,
                mama_bear_variant='scout',
                required_capabilities=['function_calling', 'code']
            )
            
            if plan_result['success']:
                # Execute through Scrapybara
                execution_result = await self.scrapybara.execute_scout_task(
                    task_description=task_description,
                    plan=plan_result['response'],
                    progress_callback=progress_callback
                )
                
                return {
                    'success': True,
                    'plan': plan_result['response'],
                    'execution': execution_result,
                    'metadata': {
                        'model_used': plan_result['model_used'],
                        'task_duration': execution_result.get('duration', 0)
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Task planning failed',
                    'details': plan_result
                }
                
        except Exception as e:
            logger.error(f"Autonomous task error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_variant_greeting(self, page_context: str) -> str:
        """Get a personalized greeting from the appropriate Mama Bear variant"""
        
        variant = self.variants.get(page_context, self.variants['main_chat'])
        
        greetings = {
            'ResearchSpecialist': "🐻 Research Specialist Mama Bear here! I'm excited to dive deep into whatever you're curious about. What shall we explore together?",
            'DevOpsSpecialist': "🐻 DevOps Specialist Mama Bear reporting for duty! I'll keep your systems running smoothly and securely. What can I help optimize today?",
            'ScoutCommander': "🐻 Scout Commander Mama Bear ready for autonomous adventures! Give me a mission and I'll handle it from start to finish. What shall we accomplish?",
            'ModelCoordinator': "🐻 Model Coordinator Mama Bear at your service! I know all the AI models and their strengths. Which one would be perfect for your task?",
            'ToolCurator': "🐻 Tool Curator Mama Bear here with endless enthusiasm for great tools! Let's find exactly what you need to supercharge your workflow!",
            'IntegrationArchitect': "🐻 Integration Architect Mama Bear ready to build solid connections! Whether it's APIs, workflows, or data - let's integrate it beautifully!",
            'LiveAPISpecialist': "🐻 Live API Specialist Mama Bear energized for real-time magic! Voice, video, streaming data - let's make it responsive and amazing!"
        }
        
        variant_name = variant.__class__.__name__
        return greetings.get(variant_name, "🐻 Mama Bear is here and ready to help with whatever you need! ✨")