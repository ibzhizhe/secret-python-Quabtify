"""错误处理工具"""
import functools
import logging
from typing import Callable, Any, TypeVar

T = TypeVar('T')

logger = logging.getLogger(__name__)


class TradingError(Exception):
    """交易系统错误基类"""
    pass


class APIError(TradingError):
    """API调用错误"""
    pass


class ValidationError(TradingError):
    """参数验证错误"""
    pass


def handle_api_error(func: Callable[..., T]) -> Callable[..., T]:
    """API错误处理装饰器"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API错误 - {func.__name__}: {str(e)}")
            raise APIError(f"API调用失败: {str(e)}")

    return wrapper
