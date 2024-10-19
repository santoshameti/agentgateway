import unittest
from typing import Dict, Any
from unittest.mock import patch, MagicMock
from core.abstract_agent import AbstractAgent
from core.conversation_manager import ConversationManager
from core.redis_conversation_manager import RedisConversationManager
from core.dynamo_conversation_manager import DynamoConversationManager
import os


class MockAgent(AbstractAgent):
    def run(self, agent_input, is_tool_response=False, conversation_id=None):
        pass

    def get_auth(self) -> Dict[str, Any]:
        pass

    def set_auth(self, auth: Dict[str, Any]):
        pass

    def get_model_config(self) -> Dict[str, Any]:
        pass

    def set_model_config(self, model_config: Dict[str, Any]):
        pass

class TestAbstractAgentConversationManager(unittest.TestCase):
    @patch('core.abstract_agent.ConfigManager')
    def setUp(self, mock_config_manager):
        self.mock_config = mock_config_manager.return_value
        self.mock_config.get_nested.side_effect = lambda *args, **kwargs: {
            ('default', 'conversation_manager'): 'in_memory',
            ('default', 'model_id'): 'test-model',
            ('default', 'max_tokens'): 2000,
            ('default', 'temperature'): 0.7,
            ('memory_redis', 'conversation_manager'): 'redis',
            ('memory_redis', 'redis_url'): 'redis://localhost:6379',
            ('memory_dynamodb', 'conversation_manager'): 'dynamodb',
            ('memory_dynamodb', 'dynamodb_table'): 'test_conversations',
            ('memory_dynamodb', 'dynamodb_region'): 'us-west-2',
        }.get(args, kwargs.get('default'))

    def tearDown(self):
        if 'AGENT_MEMORY_CONFIG_PROFILE' in os.environ:
            del os.environ['AGENT_MEMORY_CONFIG_PROFILE']

    def test_default_conversation_manager(self):
        agent = MockAgent()
        self.assertIsInstance(agent.conversation_manager, ConversationManager)
        self.assertEqual(agent.model_config['max_tokens'], 2000)
        self.assertEqual(agent.model_config['temperature'], 0.7)

    def test_redis_conversation_manager(self):
        os.environ['AGENT_MEMORY_CONFIG_PROFILE'] = 'memory_redis'
        agent = MockAgent()
        self.assertIsInstance(agent.conversation_manager, RedisConversationManager)

    def test_dynamodb_conversation_manager(self):
        os.environ['AGENT_MEMORY_CONFIG_PROFILE'] = 'memory_dynamodb'
        agent = MockAgent()
        self.assertIsInstance(agent.conversation_manager, DynamoConversationManager)

    def test_nonexistent_profile(self):
        os.environ['AGENT_CONFIG_PROFILE'] = 'nonexistent'
        agent = MockAgent()
        self.assertIsInstance(agent.conversation_manager, ConversationManager)  # Should fall back to default

class TestConversationManager(unittest.TestCase):
    @patch('core.abstract_agent.ConfigManager')
    def setUp(self, mock_config_manager):
        self.mock_config = mock_config_manager.return_value
        self.mock_config.get_nested.side_effect = lambda *args, **kwargs: {
            ('default', 'conversation_manager'): 'in_memory',
            ('redis', 'conversation_manager'): 'redis',
            ('redis', 'redis_url'): 'redis://localhost:6379',
            ('dynamodb', 'conversation_manager'): 'dynamodb',
            ('dynamodb', 'dynamodb_table'): 'test_conversations',
            ('dynamodb', 'dynamodb_region'): 'us-west-2',
        }.get(args, kwargs.get('default'))

        self.agent_in_memory = MockAgent()
        os.environ['AGENT_CONFIG_PROFILE'] = 'redis'
        self.agent_redis = MockAgent()
        os.environ['AGENT_CONFIG_PROFILE'] = 'dynamodb'
        self.agent_dynamo = MockAgent()

    def tearDown(self):
        if 'AGENT_CONFIG_PROFILE' in os.environ:
            del os.environ['AGENT_CONFIG_PROFILE']

    def test_start_conversation(self):
        for agent in [self.agent_in_memory, self.agent_redis, self.agent_dynamo]:
            conversation_id = agent.start_conversation()
            self.assertIsNotNone(conversation_id)
            self.assertTrue(isinstance(conversation_id, str))

    def test_add_to_conversation_history(self):
        for agent in [self.agent_in_memory, self.agent_redis, self.agent_dynamo]:
            conversation_id = agent.start_conversation()
            message = {"role": "user", "content": "Hello, AI!"}
            agent.add_to_conversation_history(message, conversation_id)
            history = agent.get_conversation_history(conversation_id)
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0], message)

    def test_extend_conversation_history(self):
        for agent in [self.agent_in_memory, self.agent_redis, self.agent_dynamo]:
            conversation_id = agent.start_conversation()
            messages = [
                {"role": "user", "content": "Hello, AI!"},
                {"role": "assistant", "content": "Hello! How can I assist you today?"}
            ]
            agent.extend_conversation_history(messages, conversation_id)
            history = agent.get_conversation_history(conversation_id)
            self.assertEqual(len(history), 2)
            self.assertEqual(history, messages)

    def test_clear_conversation_history(self):
        for agent in [self.agent_in_memory, self.agent_redis, self.agent_dynamo]:
            conversation_id = agent.start_conversation()
            message = {"role": "user", "content": "Hello, AI!"}
            agent.add_to_conversation_history(message, conversation_id)
            agent.clear_conversation_history(conversation_id)
            history = agent.get_conversation_history(conversation_id)
            self.assertEqual(len(history), 0)

    def test_get_formatted_conversation_history(self):
        for agent in [self.agent_in_memory, self.agent_redis, self.agent_dynamo]:
            conversation_id = agent.start_conversation()
            messages = [
                {"role": "user", "content": "Hello, AI!"},
                {"role": "assistant", "content": "Hello! How can I assist you today?"}
            ]
            agent.extend_conversation_history(messages, conversation_id)
            formatted_history = agent.get_formatted_conversation_history(conversation_id)
            expected_formatted_history = "User: Hello, AI!\nAssistant: Hello! How can I assist you today?"
            self.assertEqual(formatted_history, expected_formatted_history)


if __name__ == '__main__':
    unittest.main()