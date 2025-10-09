"""
LangChain 最简单的测试代码
"""

from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class SimpleParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        return text.strip()


def test_langchain():
    # 创建简单的提示模板
    template = "你好，{name}！今天天气如何？"
    prompt = PromptTemplate(input_variables=["name"], template=template)

    # 格式化提示
    result = prompt.format(name="张三")
    print(f"格式化结果: {result}")

    # 测试解析器
    parser = SimpleParser()
    parsed = parser.parse("  这是一个测试文本  ")
    print(f"解析结果: '{parsed}'")

    print("✅ LangChain 基础功能测试通过！")


if __name__ == "__main__":
    test_langchain()
