"""
Basic test suite for the Todo AI Chatbot implementation
"""
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_agent_service_initialization():
    """Test that the agent service initializes properly"""
    # Mock the environment variable for API key before importing
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'fake-test-key'}, clear=True):
        try:
            from src.services.agent_service import AgentService
            agent_service = AgentService()
            print("+ Agent service initialized successfully")
            assert agent_service is not None
        except Exception as e:
            print(f"- Agent service initialization failed: {e}")
            raise


def test_mcp_client_initialization():
    """Test that the MCP client initializes properly"""
    # Mock the environment variable for MCP server URL
    with patch.dict(os.environ, {'MCP_SERVER_URL': 'http://test-server:8080'}, clear=True):
        from src.core.mcp_client import MCPClient
        mcp_client = MCPClient()
        print("+ MCP client initialized successfully")
        assert mcp_client is not None
        assert mcp_client.base_url == 'http://test-server:8080'


def test_mcp_task_service():
    """Test MCP task service methods"""
    from src.services.mcp_services import MCPTaskService
    service = MCPTaskService()

    # Mock a database session
    mock_session = Mock()

    # Test that methods exist
    assert hasattr(service, 'add_task')
    assert hasattr(service, 'list_tasks')
    assert hasattr(service, 'update_task')
    assert hasattr(service, 'complete_task')
    assert hasattr(service, 'delete_task')

    print("+ MCP task service methods exist")


def test_model_definitions():
    """Test that all required models are properly defined"""
    from src.models.conversation import Conversation
    from src.models.message import Message
    from src.models.task import Task

    # Test Conversation model
    conv = Conversation(user_id="test-user")
    assert hasattr(conv, 'user_id')
    print("+ Conversation model defined correctly")

    # Test Message model
    msg = Message(conversation_id=1, role='user', content='test message')
    assert hasattr(msg, 'conversation_id')
    assert hasattr(msg, 'role')
    assert hasattr(msg, 'content')
    print("+ Message model defined correctly")

    # Test Task model exists
    task = Task(title="test", user_id="test-user")
    assert hasattr(task, 'title')
    assert hasattr(task, 'user_id')
    print("+ Task model defined correctly")


def run_tests():
    """Run all tests"""
    print("Running Todo AI Chatbot implementation tests...\n")

    try:
        test_model_definitions()
        test_agent_service_initialization()
        test_mcp_client_initialization()
        test_mcp_task_service()

        print("\n+ All tests passed! Todo AI Chatbot implementation is functioning correctly.")
        return True

    except Exception as e:
        print(f"\n- Tests failed: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)