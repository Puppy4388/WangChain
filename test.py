"""
LangChain LLM 调用测试
演示如何使用 LangChain 调用大语言模型
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def get_model(provider: str = "openai") -> BaseChatModel:
    """
    初始化聊天模型

    Args:
        provider: 模型提供商 ("openai", "anthropic", "google" 等)

    Returns:
        BaseChatModel: 初始化后的聊天模型
    """
    models = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-sonnet-4-5-20250929",
    }
    model_name = models.get(provider, "gpt-4o-mini")
    return init_chat_model(model_name)


def test_simple_invoke() -> None:
    """测试简单的模型调用"""
    print("=" * 50)
    print("测试 1: 简单调用")
    print("=" * 50)

    model = get_model()
    response = model.invoke("你好，请用一句话介绍你自己。")

    print(f"模型回复: {response.content}")
    print(f"Token 使用: {response.response_metadata.get('token_usage', 'N/A')}")
    print()


def test_with_prompt_template() -> None:
    """测试使用 PromptTemplate 的模型调用"""
    print("=" * 50)
    print("测试 2: 使用 PromptTemplate")
    print("=" * 50)

    model = get_model()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的{role}。请简洁地回答问题。"),
            ("user", "{question}"),
        ]
    )

    # 使用 LCEL 链式调用
    chain = prompt | model | StrOutputParser()

    result = chain.invoke({"role": "Python 开发专家", "question": "什么是装饰器？"})

    print(f"回复: {result}")
    print()


def test_streaming() -> None:
    """测试流式输出"""
    print("=" * 50)
    print("测试 3: 流式输出")
    print("=" * 50)

    model = get_model()

    print("流式回复: ", end="", flush=True)
    for chunk in model.stream("用三句话解释什么是机器学习。"):
        print(chunk.content, end="", flush=True)
    print("\n")


def test_batch_invoke() -> None:
    """测试批量调用"""
    print("=" * 50)
    print("测试 4: 批量调用")
    print("=" * 50)

    model = get_model()

    questions = [
        "1+1等于几？",
        "Python 是什么？",
        "什么是 API？",
    ]

    responses = model.batch(questions)

    for q, r in zip(questions, responses):
        print(f"Q: {q}")
        print(f"A: {r.content}")
        print("-" * 30)
    print()


def main() -> None:
    """运行所有测试"""
    print("\nLangChain LLM 调用测试\n")

    # 检查环境变量
    if not os.environ.get("OPENAI_API_KEY"):
        print("[警告] 未设置 OPENAI_API_KEY 环境变量")
        print("请设置环境变量后重试:")
        print("  Windows: set OPENAI_API_KEY=your-api-key")
        print("  Linux/Mac: export OPENAI_API_KEY=your-api-key")
        return

    test_simple_invoke()
    test_with_prompt_template()
    test_streaming()
    test_batch_invoke()

    print("所有测试完成!")


if __name__ == "__main__":
    main()
