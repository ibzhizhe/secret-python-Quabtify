"""基础策略类"""
from abc import ABC, abstractmethod
from src.models.trade_signal import TradeSignal


class BaseStrategy(ABC):
    """交易策略基类"""

    @abstractmethod
    def analyze_market(self) -> TradeSignal:
        """分析市场并生成交易信号"""
        pass

    @abstractmethod
    def execute_trade(self, signal: TradeSignal):
        """执行交易"""
        pass

    @abstractmethod
    def should_stop_loss(self) -> bool:
        """检查是否应该止损"""
        pass
