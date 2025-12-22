"""
LangChain v1 测试代码
使用最新的 langchain-core 导入路径
"""

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def test_prompt_template():
    """测试 PromptTemplate"""
    print("=" * 50)
    print("测试 1: PromptTemplate")
    print("=" * 50)

    # 创建简单的提示模板
    template = "你好，{name}！今天天气如何？"
    prompt = PromptTemplate.from_template(template)

    # 格式化提示
    result = prompt.format(name="张三")
    print(f"格式化结果: {result}")
    print()


def test_chat_prompt_template():
    """测试 ChatPromptTemplate (LangChain v1 推荐方式)"""
    print("=" * 50)
    print("测试 2: ChatPromptTemplate")
    print("=" * 50)

    # 使用 ChatPromptTemplate - LangChain v1 推荐的方式
    prompt = ChatPromptTemplate(
        [
            ("system", "你是一个友好的助手。"),
            ("user", "{question}"),
        ]
    )

    # 格式化消息
    messages = prompt.format_messages(question="今天天气怎么样？")
    for msg in messages:
        print(f"[{msg.type}]: {msg.content}")
    print()


def test_output_parser():
    """测试 StrOutputParser"""
    print("=" * 50)
    print("测试 3: StrOutputParser")
    print("=" * 50)

    # 使用 StrOutputParser
    parser = StrOutputParser()
    parsed = parser.parse("  这是一个测试文本  ")
    print(f"解析结果: '{parsed}'")
    print()


def test_langchain():
    """运行所有测试"""
    print("\n🚀 LangChain v1 功能测试\n")

    test_prompt_template()
    test_chat_prompt_template()
    test_output_parser()

    print("✅ LangChain v1 基础功能测试通过！")


if __name__ == "__main__":
    test_langchain()
