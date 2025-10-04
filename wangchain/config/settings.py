"""
配置管理模块 - Configuration Management Module

提供安全的配置管理，支持环境变量和配置文件
Provides secure configuration management with environment variables and config files
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, ConfigDict


class LLMConfig(BaseModel):
    """
    LLM配置类 - LLM Configuration Class
    
    使用Pydantic进行配置验证，确保配置的正确性和安全性
    Uses Pydantic for configuration validation to ensure correctness and security
    """
    
    # API密钥配置 - API Key Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API密钥")
    openai_api_base: Optional[str] = Field(default=None, description="OpenAI API基础URL")
    
    # 模型配置 - Model Configuration
    model_name: str = Field(default="gpt-3.5-turbo", description="默认模型名称")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(default=2000, gt=0, description="最大token数")
    
    # 性能配置 - Performance Configuration
    request_timeout: int = Field(default=60, gt=0, description="请求超时时间（秒）")
    max_retries: int = Field(default=3, ge=0, description="最大重试次数")
    
    model_config = ConfigDict(env_prefix='WANGCHAIN_')
    
    @field_validator('openai_api_key')
    @classmethod
    def validate_api_key(cls, v):
        """验证API密钥格式 - Validate API key format"""
        if v and not v.startswith('sk-'):
            raise ValueError("OpenAI API密钥必须以'sk-'开头")
        return v


class RAGConfig(BaseModel):
    """
    RAG配置类 - RAG Configuration Class
    
    用于配置检索增强生成的相关参数
    Used to configure Retrieval-Augmented Generation parameters
    """
    
    # 向量数据库配置 - Vector Database Configuration
    vector_store_type: str = Field(default="chroma", description="向量存储类型")
    collection_name: str = Field(default="wangchain_docs", description="集合名称")
    persist_directory: str = Field(default="./data/chroma", description="持久化目录")
    
    # 检索配置 - Retrieval Configuration
    chunk_size: int = Field(default=1000, gt=0, description="文档分块大小")
    chunk_overlap: int = Field(default=200, ge=0, description="分块重叠大小")
    top_k: int = Field(default=4, gt=0, description="检索Top-K文档数")
    
    # 嵌入模型配置 - Embedding Model Configuration
    embedding_model: str = Field(default="text-embedding-ada-002", description="嵌入模型名称")


class AgentConfig(BaseModel):
    """
    Agent配置类 - Agent Configuration Class
    
    用于配置智能代理的相关参数
    Used to configure Agent parameters
    """
    
    # Agent类型配置 - Agent Type Configuration
    agent_type: str = Field(default="zero-shot-react-description", description="Agent类型")
    max_iterations: int = Field(default=10, gt=0, description="最大迭代次数")
    
    # 工具配置 - Tool Configuration
    enable_search: bool = Field(default=True, description="启用搜索工具")
    enable_calculator: bool = Field(default=True, description="启用计算器工具")
    enable_wikipedia: bool = Field(default=True, description="启用维基百科工具")
    
    # 安全配置 - Security Configuration
    enable_human_approval: bool = Field(default=False, description="启用人工审批")


class ConfigManager:
    """
    配置管理器 - Configuration Manager
    
    使用单例模式确保配置的全局一致性
    Uses Singleton pattern to ensure global configuration consistency
    """
    
    _instance = None
    
    def __new__(cls):
        """单例模式实现 - Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化配置管理器 - Initialize configuration manager"""
        if self._initialized:
            return
            
        # 加载环境变量 - Load environment variables
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
        
        # 初始化配置 - Initialize configurations
        self.llm_config = LLMConfig(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base=os.getenv('OPENAI_API_BASE'),
        )
        self.rag_config = RAGConfig()
        self.agent_config = AgentConfig()
        
        self._initialized = True
    
    def get_llm_config(self) -> LLMConfig:
        """获取LLM配置 - Get LLM configuration"""
        return self.llm_config
    
    def get_rag_config(self) -> RAGConfig:
        """获取RAG配置 - Get RAG configuration"""
        return self.rag_config
    
    def get_agent_config(self) -> AgentConfig:
        """获取Agent配置 - Get Agent configuration"""
        return self.agent_config
    
    def update_config(self, config_type: str, **kwargs) -> None:
        """
        更新配置 - Update configuration
        
        Args:
            config_type: 配置类型 ('llm', 'rag', 'agent')
            **kwargs: 配置参数
        """
        if config_type == 'llm':
            self.llm_config = LLMConfig(**{**self.llm_config.model_dump(), **kwargs})
        elif config_type == 'rag':
            self.rag_config = RAGConfig(**{**self.rag_config.model_dump(), **kwargs})
        elif config_type == 'agent':
            self.agent_config = AgentConfig(**{**self.agent_config.model_dump(), **kwargs})
        else:
            raise ValueError(f"未知的配置类型: {config_type}")
