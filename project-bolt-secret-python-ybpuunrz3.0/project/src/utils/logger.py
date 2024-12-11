"""日志工具模块"""
import logging
import os
from datetime import datetime

def setup_logger():
    """配置主日志记录器"""
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 添加处理器
    _add_handlers(logger)
    
    return logger

def get_logger(name):
    """获取命名日志记录器"""
    return logging.getLogger(name)

def _add_handlers(logger):
    """添加日志处理器"""
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(_get_formatter())
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler(
        f'logs/trading_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setFormatter(_get_formatter())
    logger.addHandler(file_handler)

def _get_formatter():
    """获取日志格式化器"""
    return logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )