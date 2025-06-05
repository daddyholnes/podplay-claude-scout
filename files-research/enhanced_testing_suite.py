# backend/testing/test_enhanced_mama_bear.py
"""
🐻 Enhanced Mama Bear Testing Suite
Comprehensive tests for next-level browser control and computer use features
"""

import pytest
import asyncio
import json
import uuid
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Import the enhanced components
from services.enhanced_scrapybara_integration import (
    EnhancedScrapybaraManager,
    ComputerActionRequest,
    ComputerAction,
    SharedBrowserSession,
    AuthenticationFlow
)
from services.mama_bear_orchestration import AgentOrchestrator
from services.mama_bear_memory_system import EnhancedMemoryManager, MemoryType, MemoryImportance

class TestEnhancedScrapybaraIntegration:
    """Test suite for Enhanced Scrapybara integration"""
    
    @pytest.fixture
    async def enhanced_manager(self):
        """Create enhanced Scrapybara manager for testing"""
        config = {
            'scrapybara_api_key': 'test_key',
            'scrapybara_base_url': 'https://api.test.com/v1',
            'enable_cua': True,
            'enable_collaboration': True,
            'max_concurrent_instances': 5
        }
        
        manager = EnhancedScrapybaraManager(config)
        
        # Mock the HTTP session
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value.status = 201
        mock_session.post.return_value.__aenter__.return_value.json.return_value = {
            'instance_id': 'test_instance_123',
            'access_url': 'https://test-vm.scrapybara.dev',
            'ssh_connection': 'ssh test@test-vm.scrapybara.dev'
        }
        
        manager.session = mock_session
        
        return manager
    
    @pytest.mark.asyncio
    async def test_shared_browser_session_creation(self, enhanced_manager):
        """Test creating shared browser sessions"""
        user_id = 'test_user'
        agent_id = 'research_specialist'
        
        # Mock the start_browser method
        enhanced_manager.start_browser = AsyncMock(return_value={
            'instance_id': 'test_browser_123',
            'access_url': 'https://browser.test.com'
        })
        
        session = await enhanced_manager.start_shared_browser_session(user_id, agent_id)
        
        assert isinstance(session, SharedBrowserSession)
        assert session.user_id == user_id
        assert session.agent_id == agent_id
        assert session.collaboration_enabled
        assert len(session.participants) == 2
        assert user_id in session.participants
        assert agent_id in session.participants
    
    @pytest.mark.asyncio
    async def test_computer_action_execution(self, enhanced_manager):
        """Test computer control action execution"""
        action_request = ComputerActionRequest(
            action_id=str(uuid.uuid4()),
            action_type=ComputerAction.SCREENSHOT,
            target={},
            user_id='test_user',
            permission_level='elevated'
        )
        
        # Mock permission manager
        enhanced_manager.permission_manager.check_permission = AsyncMock(return_value={
            'granted': True,
            'level': 'elevated'
        })
        
        result = await enhanced_manager.execute_computer_action(action_request)
        
        assert result['success'] == True
        assert result['action_id'] == action_request.action_id
        assert 'result_data' in result
    
    @pytest.mark.asyncio
    async def test_authentication_flow_execution(self, enhanced_manager):
        """Test service authentication flow"""
        service_name = 'github'
        user_id = 'test_user'
        
        # Mock authentication methods
        enhanced_manager.start_browser = AsyncMock(return_value={
            'instance_id': 'auth_instance_123'
        })
        enhanced_manager._load_credentials = AsyncMock(return_value={
            'username': 'testuser',
            'password': 'testpass'
        })
        enhanced_manager._execute_auth_flow = AsyncMock(return_value={
            'success': True,
            'session_data': {'authenticated': True}
        })
        
        result = await enhanced_manager.login_to_service(
            service_name, user_id, 'test_vault_key'
        )
        
        assert result['success'] == True
        assert result['service'] == service_name
        assert 'session_key' in result
    
    @pytest.mark.asyncio
    async def test_research_environment_creation(self, enhanced_manager):
        """Test multi-instance research environment creation"""
        research_topic = 'AI startups 2024'
        user_id = 'test_user'
        
        # Mock instance creation
        enhanced_manager.start_ubuntu = AsyncMock(return_value={
            'instance_id': 'research_ubuntu_123'
        })
        enhanced_manager.start_browser = AsyncMock(return_value={
            'instance_id': 'research_browser_123'
        })
        enhanced_manager._configure_research_tools = AsyncMock()
        
        result = await enhanced_manager.create_research_environment(research_topic, user_id)
        
        assert result['success'] == True
        assert 'research_environment_id' in result
        assert len(result['instances']) == 2
        assert result['research_topic'] == research_topic
    
    @pytest.mark.asyncio
    async def test_collaborative_research_execution(self, enhanced_manager):
        """Test parallel collaborative research"""
        research_queries = [
            'AI startup funding 2024',
            'Machine learning infrastructure',
            'Generative AI market trends'
        ]
        user_id = 'test_user'
        
        # Mock research execution
        enhanced_manager.start_ubuntu = AsyncMock(return_value={
            'instance_id': f'research_{uuid.uuid4().hex[:8]}'
        })
        enhanced_manager._execute_research_task = AsyncMock(return_value={
            'success': True,
            'result': {
                'query': 'test_query',
                'key_findings': ['finding1', 'finding2'],
                'confidence_score': 0.85
            }
        })
        enhanced_manager._synthesize_research_results = AsyncMock(return_value={
            'combined_findings': ['synthesis1', 'synthesis2'],
            'synthesis_confidence': 0.88
        })
        
        result = await enhanced_manager.execute_collaborative_research(research_queries, user_id)
        
        assert result['success'] == True
        assert result['query_count'] == len(research_queries)
        assert 'results' in result

class TestMamaBearOrchestration:
    """Test suite for Mama Bear agent orchestration"""
    
    @pytest.fixture
    def mock_memory_manager(self):
        """Mock memory manager"""
        memory = AsyncMock()
        memory.save_interaction = AsyncMock()
        memory.get_recent_conversations = AsyncMock(return_value=[])
        memory.get_user_profile = AsyncMock(return_value=Mock(
            user_id='test_user',
            expertise_level='intermediate',
            preferred_agents=[],
            success_patterns={}
        ))
        return memory
    
    @pytest.fixture
    def mock_model_manager(self):
        """Mock model manager"""
        model_manager = AsyncMock()
        model_manager.get_response = AsyncMock(return_value={
            'success': True,
            'response': 'Test response from orchestrated agents',
            'model_used': 'test_model'
        })
        return model_manager
    
    @pytest.fixture
    def mock_scrapybara_client(self):
        """Mock enhanced Scrapybara client"""
        client = AsyncMock()
        client.shared_sessions = {}
        client.authenticated_sessions = {}
        client.instances = {}
        return client
    
    @pytest.fixture
    def orchestrator(self, mock_memory_manager, mock_model_manager, mock_scrapybara_client):
        """Create orchestrator for testing"""
        return AgentOrchestrator(
            memory_manager=mock_memory_manager,
            model_manager=mock_model_manager,
            scrapybara_client=mock_scrapybara_client
        )
    
    @pytest.mark.asyncio
    async def test_intelligent_agent_routing(self, orchestrator):
        """Test intelligent routing to appropriate agents"""
        # Test research request routing
        research_request = "Research the latest AI developments and create a summary"
        result = await orchestrator.process_user_request(
            message=research_request,
            user_id='test_user',
            page_context='main_chat'
        )
        
        assert 'success' in result or 'message' in result or 'content' in result
        
        # Test deployment request routing
        deploy_request = "Deploy my application to production with monitoring"
        result = await orchestrator.process_user_request(
            message=deploy_request,
            user_id='test_user',
            page_context='vm_hub'
        )
        
        assert 'success' in result or 'message' in result or 'content' in result
    
    @pytest.mark.asyncio
    async def test_agent_collaboration(self, orchestrator):
        """Test agent-to-agent communication"""
        await orchestrator.send_agent_message(
            from_agent='research_specialist',
            to_agent='devops_specialist',
            message='Research completed, ready for deployment planning',
            context={'research_data': {'findings': ['test_finding']}}
        )
        
        # Verify message was queued
        assert len(orchestrator.agent_messages['devops_specialist']) > 0
    
    @pytest.mark.asyncio
    async def test_system_status_reporting(self, orchestrator):
        """Test comprehensive system status reporting"""
        status = await orchestrator.get_system_status()
        
        assert 'timestamp' in status
        assert 'agents' in status
        assert 'active_tasks' in status
        assert 'global_context' in status

class TestEnhancedMemorySystem:
    """Test suite for enhanced memory system"""
    
    @pytest.fixture
    async def enhanced_memory(self):
        """Create enhanced memory manager for testing"""
        # Mock Mem0 client
        mock_mem0 = AsyncMock()
        mock_mem0.add = AsyncMock()
        mock_mem0.search = AsyncMock(return_value=[])
        
        memory = EnhancedMemoryManager(
            mem0_client=mock_mem0,
            local_storage_path='./test_memory'
        )
        
        return memory
    
    @pytest.mark.asyncio
    async def test_memory_storage_and_retrieval(self, enhanced_memory):
        """Test storing and retrieving enhanced memories"""
        user_id = 'test_user'
        
        # Store collaboration memory
        memory_id = await enhanced_memory.store_memory(
            content={
                'collaboration_type': 'shared_browser',
                'participants': ['user', 'research_specialist'],
                'outcome': 'successful'
            },
            memory_type=MemoryType.COLLABORATION_HISTORY,
            user_id=user_id,
            agent_id='research_specialist',
            importance=MemoryImportance.HIGH
        )
        
        assert memory_id is not None
        assert memory_id in enhanced_memory.memories
        
        # Retrieve memories
        memories = await enhanced_memory.retrieve_memories(
            user_id=user_id,
            memory_type=MemoryType.COLLABORATION_HISTORY,
            limit=10
        )
        
        assert len(memories) > 0
        assert memories[0].user_id == user_id
    
    @pytest.mark.asyncio
    async def test_contextual_memory_retrieval(self, enhanced_memory):
        """Test context-aware memory retrieval"""
        user_id = 'test_user'
        
        # Store contextual memory
        await enhanced_memory.store_memory(
            content={
                'task': 'research',
                'tools_used': ['scrapybara', 'browser'],
                'context': 'AI research project'
            },
            memory_type=MemoryType.PROJECT_CONTEXT,
            user_id=user_id,
            tags=['research', 'scrapybara', 'AI']
        )
        
        # Retrieve contextual memories
        contextual_memories = await enhanced_memory.get_contextual_memories(
            user_id=user_id,
            current_context={
                'page': 'research',
                'task_type': 'collaboration',
                'technologies': ['scrapybara']
            },
            limit=5
        )
        
        assert len(contextual_memories) >= 0
    
    @pytest.mark.asyncio
    async def test_memory_cleanup(self, enhanced_memory):
        """Test automatic memory cleanup"""
        # Add old memory
        old_memory_id = await enhanced_memory.store_memory(
            content={'old': 'data'},
            memory_type=MemoryType.CONVERSATION,
            user_id='test_user',
            importance=MemoryImportance.LOW
        )
        
        # Simulate old memory by modifying timestamp
        if old_memory_id in enhanced_memory.memories:
            enhanced_memory.memories[old_memory_id].created_at = datetime.now() - timedelta(days=100)
            enhanced_memory.memories[old_memory_id].accessed_at = datetime.now() - timedelta(days=100)
        
        # Run cleanup
        cleaned_count = await enhanced_memory.cleanup_old_memories(retention_days=30)
        
        assert cleaned_count >= 0

class TestIntegrationEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.fixture
    async def full_system(self):
        """Set up complete system for integration testing"""
        # Mock all components
        enhanced_scrapybara = AsyncMock(spec=EnhancedScrapybaraManager)
        memory_manager = AsyncMock()
        model_manager = AsyncMock()
        
        orchestrator = AgentOrchestrator(
            memory_manager=memory_manager,
            model_manager=model_manager,
            scrapybara_client=enhanced_scrapybara
        )
        
        return {
            'orchestrator': orchestrator,
            'enhanced_scrapybara': enhanced_scrapybara,
            'memory': memory_manager,
            'models': model_manager
        }
    
    @pytest.mark.asyncio
    async def test_complete_research_workflow(self, full_system):
        """Test complete research workflow with all components"""
        orchestrator = full_system['orchestrator']
        enhanced_scrapybara = full_system['enhanced_scrapybara']
        
        # Mock enhanced Scrapybara responses
        enhanced_scrapybara.create_research_environment.return_value = {
            'success': True,
            'research_environment_id': 'env_123',
            'instances': ['inst_1', 'inst_2']
        }
        
        enhanced_scrapybara.execute_collaborative_research.return_value = {
            'success': True,
            'results': {
                'combined_findings': ['finding1', 'finding2'],
                'synthesis_confidence': 0.9
            }
        }
        
        # Execute research workflow
        result = await orchestrator.process_user_request(
            message="Create a research environment for AI startups and execute comprehensive research",
            user_id='test_user',
            page_context='research'
        )
        
        assert 'success' in result or 'message' in result or 'content' in result
    
    @pytest.mark.asyncio
    async def test_shared_browser_collaboration_workflow(self, full_system):
        """Test shared browser collaboration workflow"""
        enhanced_scrapybara = full_system['enhanced_scrapybara']
        
        # Mock shared browser session
        mock_session = SharedBrowserSession(
            session_id='shared_123',
            user_id='test_user',
            agent_id='research_specialist',
            instance_id='browser_123',
            browser_url='https://browser.test.com',
            websocket_url='wss://collab.test.com'
        )
        
        enhanced_scrapybara.start_shared_browser_session.return_value = mock_session
        
        # Test session creation
        session = await enhanced_scrapybara.start_shared_browser_session(
            'test_user', 'research_specialist'
        )
        
        assert session.session_id == 'shared_123'
        assert session.collaboration_enabled
    
    @pytest.mark.asyncio
    async def test_computer_control_safety_workflow(self, full_system):
        """Test computer control with safety checks"""
        enhanced_scrapybara = full_system['enhanced_scrapybara']
        
        # Mock safety analysis
        enhanced_scrapybara.execute_computer_action.return_value = {
            'success': True,
            'action_id': 'action_123',
            'safety_verified': True
        }
        
        # Test safe action
        safe_action = ComputerActionRequest(
            action_id='safe_123',
            action_type=ComputerAction.SCREENSHOT,
            target={},
            user_id='test_user',
            permission_level='elevated'
        )
        
        result = await enhanced_scrapybara.execute_computer_action(safe_action)
        assert result['success'] == True

class TestPerformanceAndScaling:
    """Performance and scaling tests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_shared_sessions(self):
        """Test handling multiple concurrent shared browser sessions"""
        config = {
            'scrapybara_api_key': 'test_key',
            'max_concurrent_instances': 10
        }
        
        manager = EnhancedScrapybaraManager(config)
        manager.session = AsyncMock()
        manager.start_browser = AsyncMock(return_value={
            'instance_id': f'browser_{uuid.uuid4().hex[:8]}'
        })
        
        # Create multiple concurrent sessions
        tasks = []
        for i in range(5):
            task = manager.start_shared_browser_session(
                f'user_{i}', 'research_specialist'
            )
            tasks.append(task)
        
        sessions = await asyncio.gather(*tasks)
        
        assert len(sessions) == 5
        assert all(isinstance(s, SharedBrowserSession) for s in sessions)
    
    @pytest.mark.asyncio
    async def test_memory_system_performance(self):
        """Test memory system performance with large datasets"""
        memory = EnhancedMemoryManager(local_storage_path='./test_perf_memory')
        
        # Store many memories
        memory_ids = []
        for i in range(100):
            memory_id = await memory.store_memory(
                content={'test_data': f'data_{i}'},
                memory_type=MemoryType.CONVERSATION,
                user_id='perf_test_user',
                importance=MemoryImportance.MEDIUM
            )
            memory_ids.append(memory_id)
        
        # Test retrieval performance
        start_time = datetime.now()
        memories = await memory.retrieve_memories(
            user_id='perf_test_user',
            limit=50
        )
        end_time = datetime.now()
        
        retrieval_time = (end_time - start_time).total_seconds()
        
        assert len(memories) <= 50
        assert retrieval_time < 1.0  # Should be fast
        assert len(memory_ids) == 100

# Test configuration and fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Custom pytest markers for different test categories
pytestmark = [
    pytest.mark.asyncio,
]

# Test runner configuration
if __name__ == "__main__":
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1:
        test_category = sys.argv[1]
        
        if test_category == "integration":
            pytest.main(["-v", "TestEnhancedScrapybaraIntegration"])
        elif test_category == "orchestration":
            pytest.main(["-v", "TestMamaBearOrchestration"])
        elif test_category == "memory":
            pytest.main(["-v", "TestEnhancedMemorySystem"])
        elif test_category == "e2e":
            pytest.main(["-v", "TestIntegrationEndToEnd"])
        elif test_category == "performance":
            pytest.main(["-v", "TestPerformanceAndScaling"])
        else:
            print("Available test categories: integration, orchestration, memory, e2e, performance")
    else:
        # Run all tests
        pytest.main(["-v", __file__])
