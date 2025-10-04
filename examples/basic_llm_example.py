"""
基础LLM使用示例 - Basic LLM Usage Example

展示如何使用WangChain创建和使用LLM
Demonstrates how to create and use LLM with WangChain
"""

import os
from wangchain.core.llm_factory import LLMFactory, LLMBuilder
from wangchain.config.settings import ConfigManager


def basic_llm_example():
    """基础LLM示例 - Basic LLM example"""
    
    print("=== 基础LLM使用示例 Basic LLM Usage Example ===\n")
    
    # 方法1: 使用工厂模式创建LLM - Method 1: Create LLM using Factory pattern
    print("方法1: 使用工厂模式 Method 1: Using Factory pattern")
    llm = LLMFactory.create_llm(
        model_type="openai",
        temperature=0.7,
        model_name="gpt-3.5-turbo"
    )
    
    # 测试LLM - Test LLM
    if os.getenv('OPENAI_API_KEY'):
        response = llm.invoke("你好，请用一句话介绍LangChain。Hello, please introduce LangChain in one sentence.")
        print(f"响应 Response: {response.content}\n")
    else:
        print("提示：需要设置OPENAI_API_KEY环境变量 Note: Need to set OPENAI_API_KEY environment variable\n")
    
    # 方法2: 使用构建器模式创建LLM - Method 2: Create LLM using Builder pattern
    print("方法2: 使用构建器模式 Method 2: Using Builder pattern")
    llm_builder = (LLMBuilder()
                   .set_model_type("openai")
                   .set_temperature(0.5)
                   .set_max_tokens(1000)
                   .set_model_name("gpt-3.5-turbo"))
    
    llm2 = llm_builder.build()
    print(f"LLM创建成功 LLM created successfully: {type(llm2).__name__}\n")
    
    # 查看配置 - View configuration
    config_manager = ConfigManager()
    llm_config = config_manager.get_llm_config()
    print(f"当前LLM配置 Current LLM config:")
    print(f"  模型名称 Model name: {llm_config.model_name}")
    print(f"  温度 Temperature: {llm_config.temperature}")
    print(f"  最大tokens Max tokens: {llm_config.max_tokens}")


if __name__ == "__main__":
    basic_llm_example()
