"""
RAG示例 - RAG Example

展示如何使用WangChain进行文档检索和问答
Demonstrates how to use WangChain for document retrieval and Q&A
"""

import os
from pathlib import Path
from wangchain.rag.retriever import RAGRetriever
from wangchain.rag.chain import RAGChain


def create_sample_documents():
    """创建示例文档 - Create sample documents"""
    data_dir = Path("./data/docs")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建示例文本文件 - Create sample text files
    doc1_path = data_dir / "langchain_intro.txt"
    with open(doc1_path, 'w', encoding='utf-8') as f:
        f.write("""
LangChain简介 - Introduction to LangChain

LangChain是一个用于开发由语言模型驱动的应用程序的框架。它提供了以下核心功能：

1. LLM集成：支持多种大语言模型的集成和调用
2. 提示模板：提供灵活的提示词模板系统
3. 链式调用：支持将多个组件链接在一起
4. 代理工具：提供智能代理和工具使用能力
5. 记忆系统：支持对话历史和上下文管理

LangChain is a framework for developing applications powered by language models. It provides:

1. LLM Integration: Support for integrating and calling multiple large language models
2. Prompt Templates: Flexible prompt template system
3. Chains: Support for linking multiple components together
4. Agents and Tools: Intelligent agents with tool usage capabilities
5. Memory: Conversation history and context management
        """)
    
    doc2_path = data_dir / "rag_intro.txt"
    with open(doc2_path, 'w', encoding='utf-8') as f:
        f.write("""
RAG技术介绍 - Introduction to RAG

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合检索和生成的技术。

工作流程 Workflow:
1. 文档加载：将文档加载到系统中
2. 文本分割：将长文档分割成小块
3. 向量化：将文本转换为向量表示
4. 存储索引：将向量存储到向量数据库
5. 检索：根据查询检索相关文档
6. 生成：结合检索结果生成答案

优势 Advantages:
- 提高答案准确性 Improve answer accuracy
- 减少幻觉问题 Reduce hallucination
- 支持知识更新 Support knowledge updates
        """)
    
    return [str(doc1_path), str(doc2_path)]


def rag_example():
    """RAG示例 - RAG example"""
    
    print("=== RAG使用示例 RAG Usage Example ===\n")
    
    # 创建示例文档 - Create sample documents
    print("1. 创建示例文档 Creating sample documents...")
    doc_paths = create_sample_documents()
    print(f"   已创建 {len(doc_paths)} 个文档 Created {len(doc_paths)} documents\n")
    
    # 初始化RAG检索器 - Initialize RAG retriever
    print("2. 初始化RAG检索器 Initializing RAG retriever...")
    retriever = RAGRetriever(
        vector_store_type="chroma",
        embedding_model="text-embedding-ada-002"
    )
    
    # 加载并索引文档 - Load and index documents
    print("3. 加载并索引文档 Loading and indexing documents...")
    try:
        retriever.load_and_index_documents(doc_paths)
        print("   文档索引完成 Document indexing completed\n")
    except Exception as e:
        print(f"   错误 Error: {e}")
        print("   提示：需要设置OPENAI_API_KEY Note: Need to set OPENAI_API_KEY\n")
        return
    
    # 测试检索 - Test retrieval
    print("4. 测试检索 Testing retrieval...")
    query = "什么是RAG？What is RAG?"
    print(f"   查询 Query: {query}")
    
    try:
        docs = retriever.retrieve(query, top_k=2)
        print(f"   检索到 {len(docs)} 个相关文档 Retrieved {len(docs)} relevant documents")
        for i, doc in enumerate(docs, 1):
            print(f"\n   文档 {i} Document {i}:")
            print(f"   {doc.page_content[:200]}...")
    except Exception as e:
        print(f"   检索错误 Retrieval error: {e}")
    
    # 测试RAG问答链 - Test RAG Q&A chain
    if os.getenv('OPENAI_API_KEY'):
        print("\n5. 测试RAG问答链 Testing RAG Q&A chain...")
        try:
            rag_chain = RAGChain(retriever=retriever)
            result = rag_chain.query("LangChain有哪些核心功能？What are the core features of LangChain?")
            
            print(f"\n   问题 Question: LangChain有哪些核心功能？")
            print(f"   回答 Answer: {result['answer']}")
            print(f"\n   来源文档数 Source documents: {len(result['source_documents'])}")
        except Exception as e:
            print(f"   问答错误 Q&A error: {e}")
    else:
        print("\n5. 提示：需要OPENAI_API_KEY才能使用RAG问答链")
        print("   Note: Need OPENAI_API_KEY to use RAG Q&A chain")


if __name__ == "__main__":
    rag_example()
