# WangChain

<div align="center">

**基于LangChain的企业级LLM应用开发框架**

**Enterprise-Grade LLM Application Development Framework Based on LangChain**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

## 📖 简介 | Introduction

WangChain是一个基于LangChain构建的企业级大语言模型(LLM)应用开发框架。它采用面向对象编程和设计模式，提供高性能、高可用性、安全可靠的解决方案。

WangChain is an enterprise-grade Large Language Model (LLM) application development framework built on LangChain. It employs object-oriented programming and design patterns to provide high-performance, high-availability, and secure solutions.

## ✨ 核心特性 | Key Features

### 🏗️ 设计模式 | Design Patterns
- **工厂模式 Factory Pattern**: 灵活创建不同类型的LLM实例
- **构建器模式 Builder Pattern**: 优雅配置复杂对象
- **单例模式 Singleton Pattern**: 全局配置管理

### 🔍 RAG技术 | RAG Technology
- **多格式文档支持 Multi-format Document Support**: PDF、TXT、DOCX等
- **向量存储 Vector Stores**: 支持Chroma、FAISS等多种向量数据库
- **智能检索 Intelligent Retrieval**: 基于语义相似度的文档检索
- **问答链 Q&A Chain**: 结合检索和生成的智能问答

### 🤖 智能代理 | Intelligent Agents
- **工具集成 Tool Integration**: 搜索、计算器、维基百科等
- **ReAct框架 ReAct Framework**: 推理和行动结合的智能决策
- **可扩展架构 Extensible Architecture**: 轻松添加自定义工具

### 🔒 企业级特性 | Enterprise Features
- **配置管理 Configuration Management**: 基于Pydantic的类型安全配置
- **错误处理 Error Handling**: 完善的异常处理和重试机制
- **日志系统 Logging System**: 统一的日志管理
- **安全性 Security**: API密钥验证、输入校验

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
# 克隆仓库 Clone repository
git clone https://github.com/Puppy4388/WangChain.git
cd WangChain

# 安装依赖 Install dependencies
pip install -r requirements.txt

# 或直接安装包 Or install package directly
pip install -e .
```

### 配置 | Configuration

1. 复制环境变量模板 Copy environment template:
```bash
cp .env.example .env
```

2. 编辑.env文件，添加你的API密钥 Edit .env file and add your API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 基础使用 | Basic Usage

#### 1. LLM基础调用 | Basic LLM Usage

```python
from wangchain.core import LLMFactory, LLMBuilder

# 方法1: 使用工厂模式 Method 1: Using Factory Pattern
llm = LLMFactory.create_llm(
    model_type="openai",
    temperature=0.7,
    model_name="gpt-3.5-turbo"
)

response = llm.invoke("你好，介绍一下LangChain")
print(response.content)

# 方法2: 使用构建器模式 Method 2: Using Builder Pattern
llm = (LLMBuilder()
       .set_model_type("openai")
       .set_temperature(0.5)
       .set_max_tokens(1000)
       .build())
```

#### 2. RAG文档问答 | RAG Document Q&A

```python
from wangchain.rag import RAGRetriever, RAGChain

# 初始化RAG检索器 Initialize RAG retriever
retriever = RAGRetriever(
    vector_store_type="chroma",
    embedding_model="text-embedding-ada-002"
)

# 加载并索引文档 Load and index documents
retriever.load_and_index_documents(["path/to/doc1.pdf", "path/to/doc2.txt"])

# 创建问答链 Create Q&A chain
rag_chain = RAGChain(retriever=retriever)

# 执行查询 Execute query
result = rag_chain.query("文档的主要内容是什么？")
print(result['answer'])
```

#### 3. 智能代理 | Intelligent Agent

```python
from wangchain.agents import AgentExecutor, AgentBuilder

# 创建Agent Create agent
agent = AgentExecutor(verbose=True)

# 执行任务 Execute task
result = agent.run("请计算123 * 456的结果，并搜索Python的最新版本")
print(result)

# 使用构建器创建自定义Agent Use builder to create custom agent
from wangchain.agents import ToolFactory

custom_agent = (AgentBuilder()
                .with_tools([
                    ToolFactory.create_calculator_tool(),
                    ToolFactory.create_search_tool()
                ])
                .set_verbose(True)
                .build())
```

## 📂 项目结构 | Project Structure

```
WangChain/
├── wangchain/              # 核心包 Core package
│   ├── __init__.py
│   ├── core/              # 核心模块 Core modules
│   │   ├── llm_factory.py # LLM工厂 LLM factory
│   │   └── __init__.py
│   ├── rag/               # RAG模块 RAG module
│   │   ├── retriever.py   # 检索器 Retriever
│   │   ├── chain.py       # 问答链 Q&A chain
│   │   └── __init__.py
│   ├── agents/            # 代理模块 Agents module
│   │   ├── agent_executor.py  # Agent执行器
│   │   ├── tools.py       # 工具集 Tools
│   │   └── __init__.py
│   ├── config/            # 配置模块 Configuration
│   │   ├── settings.py    # 配置管理 Config management
│   │   └── __init__.py
│   └── utils/             # 工具模块 Utilities
│       ├── logger.py      # 日志 Logging
│       ├── errors.py      # 错误处理 Error handling
│       └── __init__.py
├── examples/              # 示例代码 Examples
│   ├── basic_llm_example.py
│   ├── rag_example.py
│   └── agent_example.py
├── tests/                 # 测试 Tests
│   ├── test_config.py
│   ├── test_core.py
│   └── test_utils.py
├── requirements.txt       # 依赖 Dependencies
├── setup.py              # 安装配置 Setup config
├── .env.example          # 环境变量模板 Env template
└── README.md             # 文档 Documentation
```

## 🎯 设计模式应用 | Design Pattern Applications

### 工厂模式 | Factory Pattern
```python
# LLMFactory和VectorStoreFactory使用工厂模式
# LLMFactory and VectorStoreFactory use Factory pattern
llm = LLMFactory.create_llm(model_type="openai")
vector_store = VectorStoreFactory.create_vector_store(store_type="chroma", ...)
```

### 构建器模式 | Builder Pattern
```python
# LLMBuilder和AgentBuilder使用构建器模式
# LLMBuilder and AgentBuilder use Builder pattern
llm = (LLMBuilder()
       .set_model_type("openai")
       .set_temperature(0.7)
       .build())
```

### 单例模式 | Singleton Pattern
```python
# ConfigManager使用单例模式确保全局配置一致
# ConfigManager uses Singleton pattern for global config consistency
config = ConfigManager()
```

## 🧪 测试 | Testing

```bash
# 运行所有测试 Run all tests
pytest

# 运行特定测试 Run specific tests
pytest tests/test_config.py

# 显示覆盖率 Show coverage
pytest --cov=wangchain
```

## 📚 示例 | Examples

查看 `examples/` 目录获取更多示例：
Check the `examples/` directory for more examples:

- `basic_llm_example.py` - LLM基础使用 Basic LLM usage
- `rag_example.py` - RAG文档问答 RAG document Q&A
- `agent_example.py` - 智能代理使用 Intelligent agent usage

运行示例 Run examples:
```bash
python examples/basic_llm_example.py
python examples/rag_example.py
python examples/agent_example.py
```

## 🔧 配置说明 | Configuration

### LLM配置 | LLM Configuration
- `model_name`: 模型名称 Model name (default: gpt-3.5-turbo)
- `temperature`: 温度参数 Temperature (0.0-2.0)
- `max_tokens`: 最大token数 Max tokens
- `request_timeout`: 请求超时 Request timeout (seconds)
- `max_retries`: 最大重试次数 Max retries

### RAG配置 | RAG Configuration
- `vector_store_type`: 向量存储类型 Vector store type (chroma/faiss)
- `chunk_size`: 文档分块大小 Chunk size
- `chunk_overlap`: 分块重叠 Chunk overlap
- `top_k`: 检索文档数 Number of documents to retrieve

### Agent配置 | Agent Configuration
- `max_iterations`: 最大迭代次数 Max iterations
- `enable_search`: 启用搜索 Enable search tool
- `enable_calculator`: 启用计算器 Enable calculator tool
- `enable_wikipedia`: 启用维基百科 Enable Wikipedia tool

## 🤝 贡献 | Contributing

欢迎贡献！请随时提交Pull Request。
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 许可证 | License

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📮 联系方式 | Contact

- GitHub: [https://github.com/Puppy4388/WangChain](https://github.com/Puppy4388/WangChain)
- Issues: [https://github.com/Puppy4388/WangChain/issues](https://github.com/Puppy4388/WangChain/issues)

## 🙏 致谢 | Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - 核心框架 Core framework
- [OpenAI](https://openai.com/) - LLM提供商 LLM provider
- 所有贡献者 All contributors