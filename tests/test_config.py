"""
配置模块测试 - Configuration Module Tests
"""

import pytest
from wangchain.config.settings import (
    ConfigManager,
    LLMConfig,
    RAGConfig,
    AgentConfig,
)


class TestLLMConfig:
    """LLM配置测试 - LLM Configuration Tests"""
    
    def test_default_config(self):
        """测试默认配置 - Test default configuration"""
        config = LLMConfig()
        assert config.model_name == "gpt-3.5-turbo"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.request_timeout == 60
        assert config.max_retries == 3
    
    def test_custom_config(self):
        """测试自定义配置 - Test custom configuration"""
        config = LLMConfig(
            model_name="gpt-4",
            temperature=0.5,
            max_tokens=1000
        )
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000
    
    def test_api_key_validation(self):
        """测试API密钥验证 - Test API key validation"""
        # 有效的API密钥 - Valid API key
        config = LLMConfig(openai_api_key="sk-test123")
        assert config.openai_api_key == "sk-test123"
        
        # 无效的API密钥 - Invalid API key
        with pytest.raises(ValueError):
            LLMConfig(openai_api_key="invalid-key")


class TestRAGConfig:
    """RAG配置测试 - RAG Configuration Tests"""
    
    def test_default_config(self):
        """测试默认配置 - Test default configuration"""
        config = RAGConfig()
        assert config.vector_store_type == "chroma"
        assert config.collection_name == "wangchain_docs"
        assert config.chunk_size == 1000
        assert config.chunk_overlap == 200
        assert config.top_k == 4
    
    def test_custom_config(self):
        """测试自定义配置 - Test custom configuration"""
        config = RAGConfig(
            vector_store_type="faiss",
            chunk_size=500,
            top_k=3
        )
        assert config.vector_store_type == "faiss"
        assert config.chunk_size == 500
        assert config.top_k == 3


class TestAgentConfig:
    """Agent配置测试 - Agent Configuration Tests"""
    
    def test_default_config(self):
        """测试默认配置 - Test default configuration"""
        config = AgentConfig()
        assert config.agent_type == "zero-shot-react-description"
        assert config.max_iterations == 10
        assert config.enable_search is True
        assert config.enable_calculator is True
        assert config.enable_wikipedia is True
    
    def test_custom_config(self):
        """测试自定义配置 - Test custom configuration"""
        config = AgentConfig(
            max_iterations=5,
            enable_search=False
        )
        assert config.max_iterations == 5
        assert config.enable_search is False


class TestConfigManager:
    """配置管理器测试 - Configuration Manager Tests"""
    
    def test_singleton_pattern(self):
        """测试单例模式 - Test singleton pattern"""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        assert manager1 is manager2
    
    def test_get_configs(self):
        """测试获取配置 - Test getting configurations"""
        manager = ConfigManager()
        
        llm_config = manager.get_llm_config()
        assert isinstance(llm_config, LLMConfig)
        
        rag_config = manager.get_rag_config()
        assert isinstance(rag_config, RAGConfig)
        
        agent_config = manager.get_agent_config()
        assert isinstance(agent_config, AgentConfig)
    
    def test_update_config(self):
        """测试更新配置 - Test updating configuration"""
        manager = ConfigManager()
        
        # 更新LLM配置 - Update LLM config
        manager.update_config('llm', temperature=0.9)
        assert manager.get_llm_config().temperature == 0.9
        
        # 更新RAG配置 - Update RAG config
        manager.update_config('rag', top_k=5)
        assert manager.get_rag_config().top_k == 5
        
        # 无效的配置类型 - Invalid config type
        with pytest.raises(ValueError):
            manager.update_config('invalid', param=1)
