"""市场数据模型"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class MarketData:
    """市场数据类"""
    symbol: str  # 交易对
    price: Decimal  # 当前价格
    timestamp: datetime  # 时间戳
    volume: Optional[Decimal] = None  # 24小时成交量
    high_24h: Optional[Decimal] = None  # 24小时最高价
    low_24h: Optional[Decimal] = None  # 24小时最低价
    open_24h: Optional[Decimal] = None  # 24小时开盘价
    close_24h: Optional[Decimal] = None  # 24小时收盘价
