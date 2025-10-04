"""
WangChain 包设置文件 - WangChain Package Setup File
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README - Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="wangchain",
    version="0.1.0",
    author="WangChain Team",
    author_email="wangchain@example.com",
    description="基于LangChain的LLM应用开发框架 - LLM Application Framework based on LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Puppy4388/WangChain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.20",
        "langchain-openai>=0.0.5",
        "openai>=1.0.0",
        "chromadb>=0.4.22",
        "faiss-cpu>=1.7.4",
        "pypdf>=3.17.0",
        "python-docx>=1.1.0",
        "beautifulsoup4>=4.12.0",
        "html2text>=2020.1.16",
        "duckduckgo-search>=4.1.0",
        "wikipedia>=1.4.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "tenacity>=8.2.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wangchain=wangchain.cli:main",
        ],
    },
)
