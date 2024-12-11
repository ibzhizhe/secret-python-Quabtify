"""交易信号模型"""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional
from decimal import Decimal


@dataclass
class TradeSignal:
    """交易信号类"""
    signal_type: Literal['BUY', 'SELL', 'HOLD']  # 信号类型
    price: Decimal  # 信号价格
    timestamp: datetime  # 信号时间
    confidence: float = 0.0  # 信号置信度(0-1)
    volume: Optional[Decimal] = None  # 建议交易量
    reason: str = ""  # 信号产生原因
    stop_loss: Optional[Decimal] = None  # 建议止损价格
    take_profit: Optional[Decimal] = None  # 建议止盈价格
