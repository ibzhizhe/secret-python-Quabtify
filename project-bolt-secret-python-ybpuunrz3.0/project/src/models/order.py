"""订单模型"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal
from decimal import Decimal


@dataclass
class Order:
    """订单数据类"""
    symbol: str  # 交易对
    side: Literal['buy', 'sell']  # 交易方向
    order_type: Literal['market', 'limit']  # 订单类型
    size: Decimal  # 交易数量
    price: Optional[Decimal] = None  # 委托价格(限价单必填)
    timestamp: datetime = datetime.now()  # 订单时间
    status: str = 'pending'  # 订单状态
    order_id: Optional[str] = None  # 订单ID

    def to_dict(self) -> dict:
        """转换为API所需的订单格式"""
        return {
            'instId': self.symbol,
            'side': self.side,
            'ordType': self.order_type,
            'sz': str(self.size),
            'px': str(self.price) if self.price else None
        }
