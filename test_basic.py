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
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个友好的助手。"),
            ("user", "{question}"),
        ]
    )

    # 使用 invoke() 方法 - 推荐的现代方式
    prompt_value = prompt.invoke({"question": "今天天气怎么样？"})
    print(f"PromptValue 类型: {type(prompt_value).__name__}")

    # 获取格式化后的消息
    for msg in prompt_value.messages:
        print(f"[{msg.type}]: {msg.content}")
    print()


def test_output_parser():
    """测试 StrOutputParser"""
    print("=" * 50)
    print("测试 3: StrOutputParser")
    print("=" * 50)

    # 使用 StrOutputParser
    parser = StrOutputParser()
    parsed = parser.invoke("  这是一个测试文本  ")
    print(f"解析结果: '{parsed}'")
    print()


def test_lcel_chain():
    """测试 LCEL 链式调用 - LangChain 核心设计理念"""
    print("=" * 50)
    print("测试 4: LCEL 链式调用")
    print("=" * 50)

    # LCEL (LangChain Expression Language) 使用 | 运算符组合组件
    # 完整的链: prompt -> model -> output_parser
    # 这里我们演示 prompt -> output_parser (不需要真实的 LLM)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个翻译助手。"),
            ("user", "请翻译: {text}"),
        ]
    )

    output_parser = StrOutputParser()

    # 使用 | 运算符创建链
    # 注意: 完整的链通常是 prompt | model | output_parser
    # 这里仅演示 prompt | output_parser 的链式语法
    chain = prompt | (lambda x: x.to_string()) | output_parser

    # 使用 invoke() 执行整个链
    result = chain.invoke({"text": "Hello, World!"})
    print(f"链式调用结果: {result}")

    # 演示链的组成部分
    print(f"\n链的结构:")
    print(f"  1. ChatPromptTemplate - 构建提示")
    print(f"  2. (中间转换) - 将 PromptValue 转为字符串")
    print(f"  3. StrOutputParser - 解析输出")
    print()


def test_langchain():
    """运行所有测试"""
    print("\n🚀 LangChain v1 功能测试\n")

    test_prompt_template()
    test_chat_prompt_template()
    test_output_parser()
    test_lcel_chain()

    print("✅ LangChain v1 基础功能测试通过！")


if __name__ == "__main__":
    test_langchain()
