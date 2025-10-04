"""
Agent执行器实现 - Agent Executor Implementation

实现智能代理的执行逻辑
Implements the execution logic for intelligent agents
"""

from typing import List, Optional, Dict, Any
from langchain.agents import AgentExecutor as LangChainAgentExecutor
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain.agents import Tool

from wangchain.core.llm_factory import LLMFactory
from wangchain.agents.tools import ToolFactory
from wangchain.config.settings import ConfigManager


class AgentExecutor:
    """
    Agent执行器 - Agent Executor
    
    管理和执行Agent任务
    Manages and executes Agent tasks
    """
    
    # ReAct提示模板 - ReAct prompt template
    REACT_PROMPT_TEMPLATE = """回答以下问题，尽你所能。你可以使用以下工具：
Answer the following questions as best you can. You have access to the following tools:

{tools}

使用以下格式 Use the following format:

问题 Question: 你必须回答的输入问题 the input question you must answer
思考 Thought: 你应该总是思考该做什么 you should always think about what to do
行动 Action: 要采取的行动，应该是[{tool_names}]之一 the action to take, should be one of [{tool_names}]
行动输入 Action Input: 行动的输入 the input to the action
观察 Observation: 行动的结果 the result of the action
... (这个思考/行动/行动输入/观察可以重复N次 this Thought/Action/Action Input/Observation can repeat N times)
思考 Thought: 我现在知道最终答案了 I now know the final answer
最终答案 Final Answer: 对原始输入问题的最终答案 the final answer to the original input question

开始 Begin!

问题 Question: {input}
思考 Thought: {agent_scratchpad}"""
    
    def __init__(
        self,
        llm=None,
        tools: Optional[List[Tool]] = None,
        prompt_template: Optional[str] = None,
        verbose: bool = True,
    ):
        """
        初始化Agent执行器 - Initialize Agent executor
        
        Args:
            llm: LLM实例，如果为None则使用工厂创建
            tools: 工具列表，如果为None则使用默认工具
            prompt_template: 自定义提示模板
            verbose: 是否显示详细输出
        """
        self.config_manager = ConfigManager()
        self.agent_config = self.config_manager.get_agent_config()
        
        # 初始化LLM - Initialize LLM
        self.llm = llm or LLMFactory.create_llm()
        
        # 初始化工具 - Initialize tools
        self.tools = tools or ToolFactory.get_default_tools()
        
        # 设置提示模板 - Set prompt template
        template = prompt_template or self.REACT_PROMPT_TEMPLATE
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        )
        
        # 创建Agent - Create agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建执行器 - Create executor
        self.executor = LangChainAgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            max_iterations=self.agent_config.max_iterations,
            handle_parsing_errors=True,
        )
    
    def run(self, task: str) -> str:
        """
        执行任务 - Execute task
        
        Args:
            task: 任务描述
            
        Returns:
            str: 执行结果
        """
        result = self.executor.invoke({"input": task})
        return result["output"]
    
    def add_tool(self, tool: Tool) -> None:
        """
        添加工具 - Add tool
        
        Args:
            tool: 工具实例
        """
        self.tools.append(tool)
        # 重新创建agent和executor - Recreate agent and executor
        self._rebuild_executor()
    
    def _rebuild_executor(self) -> None:
        """重建执行器 - Rebuild executor"""
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.executor = LangChainAgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.executor.verbose,
            max_iterations=self.agent_config.max_iterations,
            handle_parsing_errors=True,
        )


class AgentBuilder:
    """
    Agent构建器 - Agent Builder
    
    使用构建器模式创建Agent
    Uses Builder pattern to create Agent
    """
    
    def __init__(self):
        """初始化构建器 - Initialize builder"""
        self._llm = None
        self._tools = []
        self._prompt_template = None
        self._verbose = True
    
    def with_llm(self, llm) -> 'AgentBuilder':
        """设置LLM - Set LLM"""
        self._llm = llm
        return self
    
    def with_tools(self, tools: List[Tool]) -> 'AgentBuilder':
        """设置工具 - Set tools"""
        self._tools = tools
        return self
    
    def add_tool(self, tool: Tool) -> 'AgentBuilder':
        """添加工具 - Add tool"""
        self._tools.append(tool)
        return self
    
    def with_prompt_template(self, template: str) -> 'AgentBuilder':
        """设置提示模板 - Set prompt template"""
        self._prompt_template = template
        return self
    
    def set_verbose(self, verbose: bool) -> 'AgentBuilder':
        """设置详细输出 - Set verbose"""
        self._verbose = verbose
        return self
    
    def build(self) -> AgentExecutor:
        """
        构建Agent执行器 - Build Agent executor
        
        Returns:
            AgentExecutor: 配置好的Agent执行器
        """
        return AgentExecutor(
            llm=self._llm,
            tools=self._tools if self._tools else None,
            prompt_template=self._prompt_template,
            verbose=self._verbose,
        )
