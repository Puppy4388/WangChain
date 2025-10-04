"""
RAG链实现 - RAG Chain Implementation

实现基于检索的问答链
Implements retrieval-based question-answering chain
"""

from typing import Optional, Dict, Any
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from wangchain.core.llm_factory import LLMFactory
from wangchain.rag.retriever import RAGRetriever


class RAGChain:
    """
    RAG链 - RAG Chain
    
    结合检索器和LLM实现问答功能
    Combines retriever and LLM for question-answering
    """
    
    # 默认提示模板 - Default prompt template
    DEFAULT_PROMPT_TEMPLATE = """使用以下上下文来回答问题。如果你不知道答案，就说你不知道，不要试图编造答案。
Use the following context to answer the question. If you don't know the answer, just say you don't know, don't try to make up an answer.

上下文 Context:
{context}

问题 Question: {question}

有用的回答 Helpful Answer:"""
    
    def __init__(
        self,
        retriever: RAGRetriever,
        llm = None,
        prompt_template: Optional[str] = None,
        chain_type: str = "stuff",
    ):
        """
        初始化RAG链 - Initialize RAG chain
        
        Args:
            retriever: RAG检索器实例
            llm: LLM实例，如果为None则使用工厂创建
            prompt_template: 自定义提示模板
            chain_type: 链类型 ("stuff", "map_reduce", "refine", "map_rerank")
        """
        self.retriever = retriever
        self.llm = llm or LLMFactory.create_llm()
        
        # 设置提示模板 - Set prompt template
        template = prompt_template or self.DEFAULT_PROMPT_TEMPLATE
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # 创建QA链 - Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type=chain_type,
            retriever=self.retriever.get_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        执行查询 - Execute query
        
        Args:
            question: 问题
            
        Returns:
            Dict: 包含答案和源文档的字典
        """
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }
