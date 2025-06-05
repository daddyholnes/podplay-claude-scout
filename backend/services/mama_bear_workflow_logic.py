# backend/services/mama_bear_workflow_logic.py
"""
🐻 Mama Bear Workflow Logic & Decision Engine
Defines how agents make decisions, collaborate, and execute complex workflows
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from enum import Enum
from dataclasses import dataclass, field
import logging
import re

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    SIMPLE_QUERY = "simple_query"
    RESEARCH_TASK = "research_task"
    CODE_GENERATION = "code_generation"
    DEPLOYMENT_TASK = "deployment_task"
    COMPLEX_PROJECT = "complex_project"
    TROUBLESHOOTING = "troubleshooting"
    LEARNING_SESSION = "learning_session"

class DecisionConfidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CERTAIN = "certain"

@dataclass
class WorkflowDecision:
    """Represents a decision made by the workflow engine"""
    decision_type: str
    confidence: DecisionConfidence
    reasoning: str
    selected_agents: List[str]
    estimated_complexity: int  # 1-10 scale
    estimated_duration: int  # minutes
    resource_requirements: Dict[str, Any]
    fallback_options: List[str] = field(default_factory=list)

@dataclass
class ContextualKnowledge:
    """What the system knows about the current context"""
    user_expertise_level: str = "intermediate"  # beginner, intermediate, expert
    project_type: Optional[str] = None
    current_focus: Optional[str] = None
    recent_patterns: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    success_history: Dict[str, float] = field(default_factory=dict)

class WorkflowIntelligence:
    """Core intelligence for workflow decisions and agent coordination"""
    
    def __init__(self, model_manager, memory_manager):
        self.model_manager = model_manager
        self.memory = memory_manager
        
        # Decision patterns learned over time
        self.decision_patterns = {}
        self.agent_performance_history = {}
        self.workflow_templates = self._initialize_workflow_templates()
        
        # Load historical knowledge
        asyncio.create_task(self._load_historical_patterns())
    
    def _initialize_workflow_templates(self) -> Dict[str, Dict]:
        """Initialize predefined workflow templates"""
        return {
            "simple_query": {
                "agent_sequence": ["research_specialist"],
                "max_duration": 5,
                "confidence_threshold": 0.7,
                "escalation_path": ["scout_commander"]
            },
            
            "research_deep_dive": {
                "agent_sequence": ["scout_commander", "research_specialist"],
                "collaboration_type": "sequential",
                "max_duration": 30,
                "tools_required": ["scrapybara", "web_search", "document_analysis"],
                "escalation_path": ["integration_architect"]
            },
            
            "code_feature_request": {
                "agent_sequence": ["research_specialist", "scout_commander", "devops_specialist"],
                "collaboration_type": "collaborative",
                "phases": ["analysis", "design", "implementation", "testing"],
                "max_duration": 120,
                "quality_gates": ["code_review", "testing", "documentation"]
            },
            
            "deployment_automation": {
                "agent_sequence": ["devops_specialist", "integration_architect"],
                "collaboration_type": "collaborative", 
                "tools_required": ["scrapybara", "deployment_tools"],
                "max_duration": 60,
                "safety_checks": ["backup", "rollback_plan", "monitoring"]
            },
            
            "api_integration": {
                "agent_sequence": ["integration_architect", "model_coordinator"],
                "collaboration_type": "lead_support",
                "max_duration": 45,
                "required_expertise": ["authentication", "error_handling", "testing"]
            },
            
            "tool_discovery": {
                "agent_sequence": ["tool_curator", "research_specialist"],
                "collaboration_type": "lead_support", 
                "max_duration": 20,
                "evaluation_criteria": ["functionality", "reliability", "learning_curve"]
            },
            
            "live_interaction_setup": {
                "agent_sequence": ["live_api_specialist", "integration_architect"],
                "collaboration_type": "lead_support",
                "max_duration": 30,
                "performance_requirements": ["low_latency", "high_availability"]
            }
        }
    
    async def analyze_request(self, user_message: str, context: ContextualKnowledge) -> WorkflowDecision:
        """
        Analyze a user request and determine the optimal workflow
        
        This is the core intelligence that decides:
        - Which agents should handle the request
        - How they should collaborate
        - What resources are needed
        - How complex the task is
        """
        
        # Step 1: Classify the request type
        request_type = await self._classify_request(user_message, context)
        
        # Step 2: Assess complexity and scope
        complexity_analysis = await self._assess_complexity(user_message, request_type, context)
        
        # Step 3: Select optimal agents
        agent_selection = await self._select_agents(request_type, complexity_analysis, context)
        
        # Step 4: Determine collaboration pattern
        collaboration_pattern = await self._determine_collaboration(agent_selection, complexity_analysis)
        
        # Step 5: Estimate resources and timeline
        resource_estimate = await self._estimate_resources(agent_selection, complexity_analysis)
        
        # Step 6: Build decision with confidence
        decision = WorkflowDecision(
            decision_type=request_type,
            confidence=complexity_analysis['confidence'],
            reasoning=complexity_analysis['reasoning'],
            selected_agents=agent_selection['primary_agents'],
            estimated_complexity=complexity_analysis['complexity_score'],
            estimated_duration=resource_estimate['duration_minutes'],
            resource_requirements=resource_estimate['resources'],
            fallback_options=agent_selection['fallback_agents']
        )
        
        # Step 7: Learn from this decision for future improvement
        await self._record_decision_pattern(user_message, decision, context)
        
        return decision
    
    async def _classify_request(self, message: str, context: ContextualKnowledge) -> str:
        """Classify the type of request"""
        
        message_lower = message.lower()
        
        # Pattern matching for quick classification
        patterns = {
            'simple_query': [
                r'\bwhat is\b', r'\bdefine\b', r'\bexplain\b', r'\bhow does\b'
            ],
            'research_task': [
                r'\bresearch\b', r'\binvestigate\b', r'\bfind information\b', 
                r'\bcompare\b', r'\banalyze\b'
            ],
            'code_generation': [
                r'\bcreate.*function\b', r'\bwrite.*code\b', r'\bimplement\b',
                r'\bbuild.*app\b', r'\bdevelop\b'
            ],
            'deployment_task': [
                r'\bdeploy\b', r'\bhost\b', r'\bproduction\b', r'\bserver\b'
            ],
            'troubleshooting': [
                r'\berror\b', r'\bbug\b', r'\bproblem\b', r'\bnot working\b',
                r'\bfix\b', r'\bissue\b'
            ],
            'api_integration': [
                r'\bapi\b', r'\bintegrat\b', r'\bconnect\b', r'\bwebhook\b'
            ],
            'tool_discovery': [
                r'\btool\b', r'\bsoftware\b', r'\brecommend\b', r'\bfind.*for\b'
            ]
        }
        
        for request_type, type_patterns in patterns.items():
            for pattern in type_patterns:
                if re.search(pattern, message_lower):
                    return request_type
        
        # If no pattern matches, use AI classification
        return await self._ai_classify_request(message, context)
    
    async def _ai_classify_request(self, message: str, context: ContextualKnowledge) -> str:
        """Use AI to classify ambiguous requests"""
        
        classification_prompt = f"""
        Classify this user request into one of these categories:
        - simple_query: Basic questions or information requests
        - research_task: Requires investigation or analysis
        - code_generation: Building, creating, or implementing something
        - deployment_task: Deploying, hosting, or production tasks
        - troubleshooting: Fixing problems or debugging
        - api_integration: Connecting systems or services
        - tool_discovery: Finding tools or software recommendations
        - complex_project: Multi-step project requiring multiple agents
        
        User request: "{message}"
        
        User context:
        - Expertise level: {context.user_expertise_level}
        - Recent patterns: {context.recent_patterns}
        
        Return only the category name.
        """
        
        try:
            response = await self.model_manager.generate_response(
                prompt=classification_prompt,
                model_preference="flash"  # Quick classification
            )
            
            if response['success']:
                classification = response['content'].strip().lower()
                # Validate the classification
                valid_types = [wt.value for wt in WorkflowType]
                if classification in valid_types:
                    return classification
            
        except Exception as e:
            logger.warning(f"AI classification failed: {e}")
        
        # Fallback to simple_query
        return 'simple_query'
    
    async def _assess_complexity(self, message: str, request_type: str, context: ContextualKnowledge) -> Dict[str, Any]:
        """Assess the complexity of the request"""
        
        complexity_factors = {
            'message_length': len(message.split()),
            'technical_terms': len([w for w in message.split() if len(w) > 8]),
            'question_count': message.count('?'),
            'conjunction_count': len(re.findall(r'\b(and|or|also|additionally|furthermore)\b', message.lower())),
            'code_presence': 1 if '```' in message or 'function' in message else 0,
            'url_presence': 1 if 'http' in message else 0
        }
        
        # Base complexity from request type
        type_complexity = {
            'simple_query': 2,
            'research_task': 4,
            'code_generation': 6,
            'deployment_task': 7,
            'troubleshooting': 5,
            'api_integration': 6,
            'tool_discovery': 3,
            'complex_project': 9
        }
        
        base_score = type_complexity.get(request_type, 5)
        
        # Adjust based on factors
        adjustment = (
            complexity_factors['message_length'] / 20 +
            complexity_factors['technical_terms'] / 5 +
            complexity_factors['question_count'] * 0.5 +
            complexity_factors['conjunction_count'] * 0.3 +
            complexity_factors['code_presence'] * 2 +
            complexity_factors['url_presence'] * 1
        )
        
        final_score = min(10, max(1, base_score + adjustment))
        
        # Determine confidence based on pattern matching and user history
        confidence = self._calculate_confidence(request_type, context)
        
        reasoning = f"Classified as {request_type} (complexity: {final_score}/10). "
        if final_score > 7:
            reasoning += "High complexity - multiple agents recommended."
        elif final_score > 4:
            reasoning += "Medium complexity - careful coordination needed."
        else:
            reasoning += "Low complexity - single agent should suffice."
        
        return {
            'complexity_score': int(final_score),
            'confidence': confidence,
            'reasoning': reasoning,
            'factors': complexity_factors
        }
    
    def _calculate_confidence(self, request_type: str, context: ContextualKnowledge) -> DecisionConfidence:
        """Calculate confidence in the classification"""
        
        # Check if we've seen similar patterns before
        pattern_familiarity = 0
        for pattern in context.recent_patterns:
            if pattern == request_type:
                pattern_familiarity += 1
        
        # Check success history for this type
        success_rate = context.success_history.get(request_type, 0.5)
        
        # Calculate confidence score
        confidence_score = (pattern_familiarity * 0.3) + (success_rate * 0.7)
        
        if confidence_score > 0.8:
            return DecisionConfidence.CERTAIN
        elif confidence_score > 0.6:
            return DecisionConfidence.HIGH
        elif confidence_score > 0.4:
            return DecisionConfidence.MEDIUM
        else:
            return DecisionConfidence.LOW
    
    async def _select_agents(self, request_type: str, complexity_analysis: Dict, context: ContextualKnowledge) -> Dict[str, List[str]]:
        """Select the optimal agents for the task"""
        
        # Get template if available
        template = self.workflow_templates.get(request_type, {})
        template_agents = template.get('agent_sequence', [])
        
        # Adjust based on complexity
        complexity = complexity_analysis['complexity_score']
        
        if complexity <= 3:
            # Simple task - single agent
            primary_agents = template_agents[:1] if template_agents else ['research_specialist']
        elif complexity <= 6:
            # Medium task - primary + support
            primary_agents = template_agents[:2] if len(template_agents) >= 2 else ['research_specialist', 'scout_commander']
        else:
            # Complex task - full team
            primary_agents = template_agents if template_agents else ['research_specialist', 'scout_commander', 'devops_specialist']
        
        # Consider user preferences and history
        preferred_agents = context.user_preferences.get('preferred_agents', [])
        for agent in preferred_agents:
            if agent not in primary_agents and len(primary_agents) < 3:
                primary_agents.append(agent)
        
        # Fallback options
        all_agents = ['research_specialist', 'devops_specialist', 'scout_commander', 
                     'model_coordinator', 'tool_curator', 'integration_architect', 'live_api_specialist']
        fallback_agents = [agent for agent in all_agents if agent not in primary_agents]
        
        return {
            'primary_agents': primary_agents,
            'fallback_agents': fallback_agents[:2],  # Top 2 fallbacks
            'reasoning': f"Selected {len(primary_agents)} agents based on complexity {complexity}/10"
        }
    
    async def _determine_collaboration(self, agent_selection: Dict, complexity_analysis: Dict) -> Dict[str, Any]:
        """Determine how agents should collaborate"""
        
        num_agents = len(agent_selection['primary_agents'])
        complexity = complexity_analysis['complexity_score']
        
        if num_agents == 1:
            return {
                'type': 'solo',
                'coordination': 'none',
                'communication': 'user_only'
            }
        elif num_agents == 2:
            return {
                'type': 'pair',
                'coordination': 'sequential' if complexity < 6 else 'collaborative',
                'communication': 'structured_handoff'
            }
        else:
            return {
                'type': 'team',
                'coordination': 'collaborative',
                'communication': 'shared_context',
                'leadership': agent_selection['primary_agents'][0]
            }
    
    async def _estimate_resources(self, agent_selection: Dict, complexity_analysis: Dict) -> Dict[str, Any]:
        """Estimate resources and timeline"""
        
        base_duration = {
            1: 5,   # 5 minutes for single agent
            2: 15,  # 15 minutes for pair
            3: 30   # 30 minutes for team
        }
        
        num_agents = len(agent_selection['primary_agents'])
        complexity = complexity_analysis['complexity_score']
        
        # Base duration
        duration = base_duration.get(num_agents, 45)
        
        # Adjust for complexity
        duration = duration * (1 + (complexity - 5) * 0.2)
        
        # Ensure reasonable bounds
        duration = max(2, min(120, duration))
        
        resources = {
            'compute_intensive': complexity > 7,
            'requires_web_access': 'research' in str(agent_selection),
            'requires_file_access': 'scout' in str(agent_selection),
            'requires_external_apis': 'integration' in str(agent_selection)
        }
        
        return {
            'duration_minutes': int(duration),
            'resources': resources,
            'confidence_interval': f"±{int(duration * 0.3)} minutes"
        }
    
    async def _record_decision_pattern(self, message: str, decision: WorkflowDecision, context: ContextualKnowledge):
        """Record decision patterns for learning"""
        
        pattern_key = f"{decision.decision_type}_{decision.estimated_complexity}"
        
        if pattern_key not in self.decision_patterns:
            self.decision_patterns[pattern_key] = {
                'count': 0,
                'success_rate': 0.5,
                'avg_duration': decision.estimated_duration,
                'common_agents': {}
            }
        
        pattern = self.decision_patterns[pattern_key]
        pattern['count'] += 1
        
        # Track agent selection frequency
        for agent in decision.selected_agents:
            if agent not in pattern['common_agents']:
                pattern['common_agents'][agent] = 0
            pattern['common_agents'][agent] += 1
    
    async def learn_from_outcome(self, decision: WorkflowDecision, outcome: Dict[str, Any]):
        """Learn from the outcome of a decision"""
        
        pattern_key = f"{decision.decision_type}_{decision.estimated_complexity}"
        
        if pattern_key in self.decision_patterns:
            pattern = self.decision_patterns[pattern_key]
            
            # Update success rate
            success = outcome.get('success', False)
            current_rate = pattern['success_rate']
            pattern['success_rate'] = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1
            
            # Update duration estimates
            actual_duration = outcome.get('duration_minutes', decision.estimated_duration)
            pattern['avg_duration'] = (pattern['avg_duration'] * 0.8) + (actual_duration * 0.2)
        
        # Save patterns periodically
        if sum(p['count'] for p in self.decision_patterns.values()) % 10 == 0:
            await self._save_decision_patterns()
    
    async def _load_historical_patterns(self):
        """Load historical decision patterns"""
        try:
            # This would load from persistent storage
            # For now, initialize with empty patterns
            pass
        except Exception as e:
            logger.warning(f"Could not load historical patterns: {e}")
    
    async def _save_decision_patterns(self):
        """Save decision patterns to persistent storage"""
        try:
            # This would save to persistent storage
            # For now, just log the patterns
            logger.info(f"Saving {len(self.decision_patterns)} decision patterns")
        except Exception as e:
            logger.error(f"Could not save decision patterns: {e}")
    
    async def get_workflow_recommendations(self, context: ContextualKnowledge) -> List[Dict[str, Any]]:
        """Get workflow recommendations based on context"""
        
        recommendations = []
        
        # Analyze recent patterns
        recent_types = context.recent_patterns[-5:]  # Last 5 requests
        
        for pattern_type in set(recent_types):
            if pattern_type in self.decision_patterns:
                pattern = self.decision_patterns[pattern_type]
                
                # Recommend if high success rate
                if pattern['success_rate'] > 0.8:
                    recommendations.append({
                        'type': pattern_type,
                        'success_rate': pattern['success_rate'],
                        'avg_duration': pattern['avg_duration'],
                        'recommended_agents': sorted(
                            pattern['common_agents'].items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:3]
                    })
        
        return sorted(recommendations, key=lambda x: x['success_rate'], reverse=True)[:3]

# Integration function
async def initialize_workflow_intelligence(orchestrator) -> WorkflowIntelligence:
    """Initialize the workflow intelligence system"""
    
    workflow_intelligence = WorkflowIntelligence(
        model_manager=orchestrator.model_manager,
        memory_manager=orchestrator.memory_manager
    )
    
    logger.info("🧠 Mama Bear Workflow Intelligence initialized!")
    
    return workflow_intelligence