"""策略基类"""
from abc import ABC, abstractmethod
from typing import Optional, Dict
from src.models.order import Order


class StrategyBase(ABC):
    """交易策略基类"""

    @abstractmethod
    def analyze_market(self) -> Optional[Dict]:
        """分析市场并生成交易信号"""
        pass

    @abstractmethod
    def generate_order(self, signal: Dict) -> Optional[Order]:
        """根据信号生成订单"""
        pass

    @abstractmethod
    def should_stop_loss(self) -> bool:
        """检查是否应该止损"""
        pass
