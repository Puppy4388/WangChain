"""
RAG检索器实现 - RAG Retriever Implementation

实现检索增强生成(RAG)功能，支持多种向量数据库和文档加载器
Implements Retrieval-Augmented Generation (RAG) with support for multiple vector databases and document loaders
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
from abc import ABC, abstractmethod

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_openai import OpenAIEmbeddings

from wangchain.config.settings import ConfigManager


class DocumentLoader:
    """
    文档加载器 - Document Loader
    
    支持多种文档格式的加载
    Supports loading multiple document formats
    """
    
    @staticmethod
    def load_documents(file_path: str) -> List[Document]:
        """
        加载文档 - Load documents
        
        Args:
            file_path: 文件路径
            
        Returns:
            List[Document]: 文档列表
            
        Raises:
            ValueError: 当文件格式不支持时抛出
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 根据文件扩展名选择合适的加载器 - Select appropriate loader based on file extension
        if path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(file_path)
        elif path.suffix.lower() == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif path.suffix.lower() in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {path.suffix}")
        
        return loader.load()


class VectorStoreFactory:
    """
    向量存储工厂 - Vector Store Factory
    
    使用工厂模式创建不同类型的向量存储
    Uses Factory pattern to create different types of vector stores
    """
    
    @staticmethod
    def create_vector_store(
        store_type: str,
        documents: List[Document],
        embedding_function: Any,
        **kwargs
    ):
        """
        创建向量存储 - Create vector store
        
        Args:
            store_type: 存储类型 ("chroma" 或 "faiss")
            documents: 文档列表
            embedding_function: 嵌入函数
            **kwargs: 额外参数
            
        Returns:
            向量存储实例
        """
        if store_type.lower() == "chroma":
            return Chroma.from_documents(
                documents=documents,
                embedding=embedding_function,
                **kwargs
            )
        elif store_type.lower() == "faiss":
            return FAISS.from_documents(
                documents=documents,
                embedding=embedding_function,
                **kwargs
            )
        else:
            raise ValueError(f"不支持的向量存储类型: {store_type}")


class RAGRetriever:
    """
    RAG检索器 - RAG Retriever
    
    实现完整的RAG流程：文档加载、分块、向量化、检索
    Implements complete RAG pipeline: document loading, chunking, vectorization, retrieval
    """
    
    def __init__(
        self,
        vector_store_type: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ):
        """
        初始化RAG检索器 - Initialize RAG retriever
        
        Args:
            vector_store_type: 向量存储类型
            embedding_model: 嵌入模型名称
        """
        self.config_manager = ConfigManager()
        self.rag_config = self.config_manager.get_rag_config()
        
        # 使用提供的参数或配置的默认值 - Use provided parameters or configured defaults
        self.vector_store_type = vector_store_type or self.rag_config.vector_store_type
        self.embedding_model = embedding_model or self.rag_config.embedding_model
        
        # 初始化嵌入函数 - Initialize embedding function
        self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        
        # 初始化文本分割器 - Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.rag_config.chunk_size,
            chunk_overlap=self.rag_config.chunk_overlap,
        )
        
        self.vector_store = None
    
    def load_and_index_documents(
        self,
        file_paths: List[str],
        **kwargs
    ) -> None:
        """
        加载并索引文档 - Load and index documents
        
        Args:
            file_paths: 文件路径列表
            **kwargs: 额外的向量存储参数
        """
        # 加载所有文档 - Load all documents
        all_documents = []
        for file_path in file_paths:
            documents = DocumentLoader.load_documents(file_path)
            all_documents.extend(documents)
        
        # 分割文档 - Split documents
        splits = self.text_splitter.split_documents(all_documents)
        
        # 创建向量存储 - Create vector store
        store_kwargs = {
            "collection_name": self.rag_config.collection_name,
            "persist_directory": self.rag_config.persist_directory,
        } if self.vector_store_type.lower() == "chroma" else {}
        
        store_kwargs.update(kwargs)
        
        self.vector_store = VectorStoreFactory.create_vector_store(
            store_type=self.vector_store_type,
            documents=splits,
            embedding_function=self.embeddings,
            **store_kwargs
        )
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Document]:
        """
        检索相关文档 - Retrieve relevant documents
        
        Args:
            query: 查询文本
            top_k: 返回的文档数量
            
        Returns:
            List[Document]: 相关文档列表
        """
        if self.vector_store is None:
            raise ValueError("向量存储未初始化，请先调用load_and_index_documents方法")
        
        k = top_k or self.rag_config.top_k
        return self.vector_store.similarity_search(query, k=k)
    
    def get_retriever(self, **kwargs):
        """
        获取检索器对象 - Get retriever object
        
        Returns:
            检索器对象，可用于LangChain链式调用
        """
        if self.vector_store is None:
            raise ValueError("向量存储未初始化，请先调用load_and_index_documents方法")
        
        search_kwargs = {"k": self.rag_config.top_k}
        search_kwargs.update(kwargs)
        
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
