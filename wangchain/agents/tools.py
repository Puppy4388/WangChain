"""
Agent工具实现 - Agent Tools Implementation

提供Agent可用的各种工具
Provides various tools available to Agents
"""

from typing import List
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from wangchain.config.settings import ConfigManager


class ToolFactory:
    """
    工具工厂 - Tool Factory
    
    使用工厂模式创建Agent工具
    Uses Factory pattern to create Agent tools
    """
    
    @staticmethod
    def create_search_tool() -> Tool:
        """
        创建搜索工具 - Create search tool
        
        Returns:
            Tool: DuckDuckGo搜索工具
        """
        search = DuckDuckGoSearchRun()
        return Tool(
            name="网络搜索 Web Search",
            func=search.run,
            description="当你需要搜索最新信息或查找在线资源时很有用。输入应该是一个搜索查询。Useful for when you need to search for current information or find online resources. Input should be a search query."
        )
    
    @staticmethod
    def create_wikipedia_tool() -> Tool:
        """
        创建维基百科工具 - Create Wikipedia tool
        
        Returns:
            Tool: 维基百科查询工具
        """
        wikipedia = WikipediaAPIWrapper()
        return Tool(
            name="维基百科 Wikipedia",
            func=wikipedia.run,
            description="当你需要查找概念、人物、地点或历史事件的详细信息时很有用。输入应该是一个搜索词。Useful for when you need to find detailed information about concepts, people, places, or historical events. Input should be a search term."
        )
    
    @staticmethod
    def create_calculator_tool() -> Tool:
        """
        创建计算器工具 - Create calculator tool
        
        Returns:
            Tool: Python计算器工具
        """
        def calculator(expression: str) -> str:
            """安全的数学表达式计算器 - Safe mathematical expression calculator"""
            try:
                # 仅允许数学运算，提高安全性 - Only allow math operations for security
                allowed_chars = set('0123456789+-*/(). ')
                if not all(c in allowed_chars for c in expression):
                    return "错误：表达式包含非法字符 Error: Expression contains illegal characters"
                
                result = eval(expression, {"__builtins__": {}}, {})
                return str(result)
            except Exception as e:
                return f"计算错误 Calculation error: {str(e)}"
        
        return Tool(
            name="计算器 Calculator",
            func=calculator,
            description="当你需要进行数学计算时很有用。输入应该是一个数学表达式。Useful for when you need to perform mathematical calculations. Input should be a mathematical expression."
        )
    
    @staticmethod
    def get_default_tools() -> List[Tool]:
        """
        获取默认工具集 - Get default tool set
        
        Returns:
            List[Tool]: 默认工具列表
        """
        config_manager = ConfigManager()
        agent_config = config_manager.get_agent_config()
        
        tools = []
        
        if agent_config.enable_search:
            tools.append(ToolFactory.create_search_tool())
        
        if agent_config.enable_wikipedia:
            tools.append(ToolFactory.create_wikipedia_tool())
        
        if agent_config.enable_calculator:
            tools.append(ToolFactory.create_calculator_tool())
        
        return tools
