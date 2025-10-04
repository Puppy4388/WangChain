"""
错误处理工具 - Error Handling Utilities

提供统一的错误处理和重试机制
Provides unified error handling and retry mechanisms
"""

import time
from typing import Callable, Any, Optional
from functools import wraps
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from wangchain.utils.logger import default_logger


class WangChainException(Exception):
    """WangChain基础异常类 - WangChain base exception class"""
    pass


class ConfigurationError(WangChainException):
    """配置错误 - Configuration error"""
    pass


class DocumentLoadError(WangChainException):
    """文档加载错误 - Document loading error"""
    pass


class VectorStoreError(WangChainException):
    """向量存储错误 - Vector store error"""
    pass


class AgentExecutionError(WangChainException):
    """Agent执行错误 - Agent execution error"""
    pass


def retry_on_failure(
    max_attempts: int = 3,
    wait_min: int = 1,
    wait_max: int = 10,
    exception_types: tuple = (Exception,)
):
    """
    失败重试装饰器 - Retry on failure decorator
    
    Args:
        max_attempts: 最大重试次数
        wait_min: 最小等待时间（秒）
        wait_max: 最大等待时间（秒）
        exception_types: 需要重试的异常类型
        
    Returns:
        装饰器函数
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(min=wait_min, max=wait_max),
        retry=retry_if_exception_type(exception_types),
        before_sleep=lambda retry_state: default_logger.warning(
            f"重试 Retry attempt {retry_state.attempt_number}/{max_attempts}"
        ),
    )


def handle_errors(func: Callable) -> Callable:
    """
    错误处理装饰器 - Error handling decorator
    
    捕获并记录函数执行中的错误
    Catches and logs errors during function execution
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WangChainException as e:
            default_logger.error(f"WangChain错误 WangChain error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            default_logger.error(f"未预期错误 Unexpected error in {func.__name__}: {str(e)}")
            raise WangChainException(f"执行失败 Execution failed: {str(e)}") from e
    
    return wrapper
