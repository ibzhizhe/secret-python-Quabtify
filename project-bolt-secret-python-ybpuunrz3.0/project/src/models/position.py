"""持仓模型"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Position:
    """持仓数据类"""
    symbol: str  # 交易对
    side: str  # 持仓方向(long/short)
    size: Decimal  # 持仓数量
    entry_price: Decimal  # 开仓价格
    entry_time: datetime  # 开仓时间
    unrealized_pnl: Decimal = Decimal('0')  # 未实现盈亏
    stop_loss: Optional[Decimal] = None  # 止损价格
    take_profit: Optional[Decimal] = None  # 止盈价格

    def update_pnl(self, current_price: Decimal) -> None:
        """更新未实现盈亏"""
        if self.side == 'long':
            self.unrealized_pnl = (current_price - self.entry_price) * self.size
        else:
            self.unrealized_pnl = (self.entry_price - current_price) * self.size

    def should_stop_loss(self, current_price: Decimal) -> bool:
        """检查是否触发止损"""
        if not self.stop_loss:
            return False
        if self.side == 'long':
            return current_price <= self.stop_loss
        return current_price >= self.stop_loss

    def should_take_profit(self, current_price: Decimal) -> bool:
        """检查是否触发止盈"""
        if not self.take_profit:
            return False
        if self.side == 'long':
            return current_price >= self.take_profit
        return current_price <= self.take_profit
