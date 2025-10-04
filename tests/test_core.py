"""
核心模块测试 - Core Module Tests
"""

import pytest
from unittest.mock import Mock, patch
from wangchain.core.llm_factory import LLMFactory, LLMBuilder
from langchain_openai import ChatOpenAI


class TestLLMFactory:
    """LLM工厂测试 - LLM Factory Tests"""
    
    @patch('wangchain.core.llm_factory.ChatOpenAI')
    def test_create_openai_llm(self, mock_chat_openai):
        """测试创建OpenAI LLM - Test creating OpenAI LLM"""
        mock_instance = Mock()
        mock_chat_openai.return_value = mock_instance
        
        llm = LLMFactory.create_llm(model_type="openai")
        
        # 验证返回值 - Verify return value
        assert llm == mock_instance
        mock_chat_openai.assert_called_once()
    
    def test_unsupported_model_type(self):
        """测试不支持的模型类型 - Test unsupported model type"""
        with pytest.raises(ValueError, match="不支持的模型类型"):
            LLMFactory.create_llm(model_type="unsupported")
    
    @patch('wangchain.core.llm_factory.ChatOpenAI')
    def test_create_llm_with_custom_params(self, mock_chat_openai):
        """测试使用自定义参数创建LLM - Test creating LLM with custom parameters"""
        mock_instance = Mock()
        mock_chat_openai.return_value = mock_instance
        
        llm = LLMFactory.create_llm(
            model_type="openai",
            temperature=0.9,
            max_tokens=500
        )
        
        # 验证传递的参数 - Verify passed parameters
        call_args = mock_chat_openai.call_args[1]
        assert call_args['temperature'] == 0.9
        assert call_args['max_tokens'] == 500


class TestLLMBuilder:
    """LLM构建器测试 - LLM Builder Tests"""
    
    @patch('wangchain.core.llm_factory.ChatOpenAI')
    def test_builder_pattern(self, mock_chat_openai):
        """测试构建器模式 - Test builder pattern"""
        mock_instance = Mock()
        mock_chat_openai.return_value = mock_instance
        
        builder = LLMBuilder()
        llm = (builder
               .set_model_type("openai")
               .set_temperature(0.8)
               .set_max_tokens(1500)
               .set_model_name("gpt-4")
               .build())
        
        assert llm == mock_instance
        
        # 验证构建参数 - Verify build parameters
        call_args = mock_chat_openai.call_args[1]
        assert call_args['temperature'] == 0.8
        assert call_args['max_tokens'] == 1500
        assert call_args['model_name'] == "gpt-4"
    
    @patch('wangchain.core.llm_factory.ChatOpenAI')
    def test_builder_chaining(self, mock_chat_openai):
        """测试链式调用 - Test method chaining"""
        builder = LLMBuilder()
        
        # 验证每个方法返回构建器实例 - Verify each method returns builder instance
        assert builder.set_model_type("openai") is builder
        assert builder.set_temperature(0.5) is builder
        assert builder.set_max_tokens(1000) is builder
        assert builder.set_model_name("gpt-3.5-turbo") is builder
