"""
日志工具 - Logging Utilities

提供统一的日志管理
Provides unified logging management
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class LoggerFactory:
    """
    日志工厂 - Logger Factory
    
    提供日志配置功能
    Provides logging configuration functionality
    """
    
    @staticmethod
    def setup_logger(
        name: str = "wangchain",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """
        设置日志器 - Setup logger
        
        Args:
            name: 日志器名称
            level: 日志级别
            log_file: 日志文件路径
            
        Returns:
            logging.Logger: 配置好的日志器
        """
        logger = logging.getLogger(name)
        
        # 如果logger已经有handlers，先清除（避免重复）
        # If logger already has handlers, clear them first (avoid duplication)
        if logger.handlers:
            logger.handlers.clear()
            
        logger.setLevel(level)
        
        # 控制台处理器 - Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器 - File handler
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger


# 默认日志器 - Default logger
default_logger = LoggerFactory.setup_logger()
