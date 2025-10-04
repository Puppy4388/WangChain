"""
WangChain - 基于LangChain的LLM应用框架
A LangChain-based LLM Application Framework

本包提供了一个完整的LLM应用开发框架，包含：
- RAG（检索增强生成）功能
- Agent（智能代理）功能
- 设计模式最佳实践
- 高性能和高可用性设计

This package provides a complete LLM application development framework, including:
- RAG (Retrieval-Augmented Generation) functionality
- Agent functionality
- Design pattern best practices
- High performance and high availability design
"""

__version__ = "0.1.0"
__author__ = "WangChain Team"

from wangchain.core.llm_factory import LLMFactory
from wangchain.rag.retriever import RAGRetriever
from wangchain.agents.agent_executor import AgentExecutor

__all__ = [
    "LLMFactory",
    "RAGRetriever", 
    "AgentExecutor",
]
