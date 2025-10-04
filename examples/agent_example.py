"""
Agent示例 - Agent Example

展示如何使用WangChain创建和使用智能代理
Demonstrates how to create and use intelligent agents with WangChain
"""

import os
from wangchain.agents.agent_executor import AgentExecutor, AgentBuilder
from wangchain.agents.tools import ToolFactory


def agent_example():
    """Agent示例 - Agent example"""
    
    print("=== Agent使用示例 Agent Usage Example ===\n")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("提示：需要设置OPENAI_API_KEY环境变量才能运行此示例")
        print("Note: Need to set OPENAI_API_KEY environment variable to run this example")
        return
    
    # 方法1: 直接创建Agent - Method 1: Create Agent directly
    print("方法1: 直接创建Agent Method 1: Create Agent directly\n")
    
    try:
        agent = AgentExecutor(verbose=True)
        
        # 测试计算器工具 - Test calculator tool
        print("测试1: 使用计算器 Test 1: Using calculator")
        result = agent.run("请计算 123 * 456 的结果 Please calculate 123 * 456")
        print(f"结果 Result: {result}\n")
        
        # 测试搜索工具 - Test search tool
        print("测试2: 使用搜索工具 Test 2: Using search tool")
        result = agent.run("搜索Python编程语言的最新信息 Search for latest information about Python programming language")
        print(f"结果 Result: {result}\n")
        
    except Exception as e:
        print(f"错误 Error: {e}\n")
    
    # 方法2: 使用构建器模式创建Agent - Method 2: Create Agent using Builder pattern
    print("方法2: 使用构建器模式 Method 2: Using Builder pattern\n")
    
    try:
        # 创建自定义工具集 - Create custom tool set
        custom_tools = [
            ToolFactory.create_calculator_tool(),
            ToolFactory.create_wikipedia_tool(),
        ]
        
        agent2 = (AgentBuilder()
                  .with_tools(custom_tools)
                  .set_verbose(True)
                  .build())
        
        # 测试维基百科工具 - Test Wikipedia tool
        print("测试3: 使用维基百科工具 Test 3: Using Wikipedia tool")
        result = agent2.run("查找人工智能的定义 Find the definition of Artificial Intelligence")
        print(f"结果 Result: {result}\n")
        
    except Exception as e:
        print(f"错误 Error: {e}\n")
    
    # 测试添加自定义工具 - Test adding custom tool
    print("方法3: 添加自定义工具 Method 3: Adding custom tool\n")
    
    from langchain.agents import Tool
    
    def custom_greeter(name: str) -> str:
        """自定义问候工具 - Custom greeting tool"""
        return f"你好，{name}！很高兴见到你。Hello, {name}! Nice to meet you."
    
    custom_tool = Tool(
        name="问候工具 Greeter",
        func=custom_greeter,
        description="用于问候用户的工具。输入应该是一个名字。Useful for greeting users. Input should be a name."
    )
    
    try:
        agent3 = AgentExecutor(tools=[custom_tool], verbose=True)
        result = agent3.run("请问候一下张三 Please greet Zhang San")
        print(f"结果 Result: {result}\n")
    except Exception as e:
        print(f"错误 Error: {e}\n")


if __name__ == "__main__":
    agent_example()
