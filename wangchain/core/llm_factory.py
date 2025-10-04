"""
LLM工厂模式实现 - LLM Factory Pattern Implementation

使用工厂模式创建和管理LLM实例，支持多种LLM提供商
Uses Factory pattern to create and manage LLM instances, supporting multiple LLM providers
"""

from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain.llms.base import BaseLLM
from langchain.chat_models.base import BaseChatModel

from wangchain.config.settings import ConfigManager


class LLMFactory:
    """
    LLM工厂类 - LLM Factory Class
    
    使用工厂模式创建不同类型的LLM实例
    Uses Factory pattern to create different types of LLM instances
    
    支持的模型类型:
    - OpenAI GPT models
    - 可扩展支持其他模型
    
    Supported model types:
    - OpenAI GPT models  
    - Extensible to support other models
    """
    
    @staticmethod
    def create_llm(
        model_type: str = "openai",
        **kwargs
    ) -> BaseChatModel:
        """
        创建LLM实例 - Create LLM instance
        
        Args:
            model_type: 模型类型，默认为"openai"
            **kwargs: 额外的模型参数
            
        Returns:
            BaseChatModel: LLM实例
            
        Raises:
            ValueError: 当模型类型不支持时抛出
        """
        config_manager = ConfigManager()
        llm_config = config_manager.get_llm_config()
        
        if model_type.lower() == "openai":
            return LLMFactory._create_openai_llm(llm_config, **kwargs)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")
    
    @staticmethod
    def _create_openai_llm(llm_config, **kwargs) -> ChatOpenAI:
        """
        创建OpenAI LLM实例 - Create OpenAI LLM instance
        
        Args:
            llm_config: LLM配置对象
            **kwargs: 额外参数
            
        Returns:
            ChatOpenAI: OpenAI聊天模型实例
        """
        # 合并配置和用户参数 - Merge configuration and user parameters
        params = {
            "model_name": llm_config.model_name,
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "request_timeout": llm_config.request_timeout,
            "max_retries": llm_config.max_retries,
        }
        
        # API密钥配置 - API key configuration
        if llm_config.openai_api_key:
            params["openai_api_key"] = llm_config.openai_api_key
        
        if llm_config.openai_api_base:
            params["openai_api_base"] = llm_config.openai_api_base
        
        # 用户参数覆盖默认配置 - User parameters override defaults
        params.update(kwargs)
        
        return ChatOpenAI(**params)


class LLMBuilder:
    """
    LLM构建器 - LLM Builder
    
    使用构建器模式提供更灵活的LLM配置方式
    Uses Builder pattern for more flexible LLM configuration
    """
    
    def __init__(self):
        """初始化构建器 - Initialize builder"""
        self._model_type = "openai"
        self._params = {}
    
    def set_model_type(self, model_type: str) -> 'LLMBuilder':
        """设置模型类型 - Set model type"""
        self._model_type = model_type
        return self
    
    def set_temperature(self, temperature: float) -> 'LLMBuilder':
        """设置温度参数 - Set temperature"""
        self._params["temperature"] = temperature
        return self
    
    def set_max_tokens(self, max_tokens: int) -> 'LLMBuilder':
        """设置最大token数 - Set max tokens"""
        self._params["max_tokens"] = max_tokens
        return self
    
    def set_model_name(self, model_name: str) -> 'LLMBuilder':
        """设置模型名称 - Set model name"""
        self._params["model_name"] = model_name
        return self
    
    def build(self) -> BaseChatModel:
        """
        构建LLM实例 - Build LLM instance
        
        Returns:
            BaseChatModel: 配置好的LLM实例
        """
        return LLMFactory.create_llm(self._model_type, **self._params)
