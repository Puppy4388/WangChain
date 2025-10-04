"""
工具模块测试 - Utils Module Tests
"""

import pytest
import logging
from pathlib import Path
from wangchain.utils.logger import LoggerFactory
from wangchain.utils.errors import (
    WangChainException,
    ConfigurationError,
    DocumentLoadError,
    retry_on_failure,
    handle_errors,
)


class TestLoggerFactory:
    """日志工厂测试 - Logger Factory Tests"""
    
    def test_setup_logger(self):
        """测试设置日志器 - Test setting up logger"""
        logger = LoggerFactory.setup_logger(name="test_logger")
        assert logger.name == "test_logger"
        assert isinstance(logger, logging.Logger)
    
    def test_logger_with_file(self, tmp_path):
        """测试带文件的日志器 - Test logger with file"""
        log_file = tmp_path / "test.log"
        logger = LoggerFactory.setup_logger(
            name="file_logger",
            log_file=str(log_file)
        )
        
        logger.info("Test message")
        # Flush the handlers to ensure the message is written
        for handler in logger.handlers:
            handler.flush()
        assert log_file.exists()


class TestExceptions:
    """异常测试 - Exception Tests"""
    
    def test_wangchain_exception(self):
        """测试WangChain基础异常 - Test WangChain base exception"""
        with pytest.raises(WangChainException):
            raise WangChainException("Test error")
    
    def test_configuration_error(self):
        """测试配置错误 - Test configuration error"""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Config error")
    
    def test_document_load_error(self):
        """测试文档加载错误 - Test document load error"""
        with pytest.raises(DocumentLoadError):
            raise DocumentLoadError("Load error")
    
    def test_exception_inheritance(self):
        """测试异常继承 - Test exception inheritance"""
        assert issubclass(ConfigurationError, WangChainException)
        assert issubclass(DocumentLoadError, WangChainException)


class TestErrorHandling:
    """错误处理测试 - Error Handling Tests"""
    
    def test_handle_errors_decorator(self):
        """测试错误处理装饰器 - Test error handling decorator"""
        
        @handle_errors
        def test_function():
            raise ValueError("Test error")
        
        with pytest.raises(WangChainException):
            test_function()
    
    def test_handle_errors_with_wangchain_exception(self):
        """测试处理WangChain异常 - Test handling WangChain exception"""
        
        @handle_errors
        def test_function():
            raise ConfigurationError("Config error")
        
        with pytest.raises(ConfigurationError):
            test_function()
    
    def test_retry_decorator(self):
        """测试重试装饰器 - Test retry decorator"""
        
        call_count = 0
        
        @retry_on_failure(max_attempts=3, wait_min=0, wait_max=0)
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "Success"
        
        result = flaky_function()
        assert result == "Success"
        assert call_count == 3
