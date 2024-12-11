"""简单交易策略实现"""
from decimal import Decimal
import numpy as np
from datetime import datetime
from typing import Optional, Dict
from src.strategy.strategy_base import StrategyBase
from src.models.order import Order
from src.models.position import Position
from src.utils.market_utils import calculate_price_change
from src.constants.trading_constants import (
    TRADE_SIDES,
    ORDER_TYPES,
    DEFAULT_TRADE_SIZE
)


class SimpleStrategy(StrategyBase):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.position: Optional[Position] = None

    def analyze_market(self) -> Optional[Dict]:
        """分析市场生成交易信号"""
        ticker = self.client.get_ticker(self.config.SYMBOL)
        if not ticker:
            return None

        # 示例策略：随机生成交易信号
        signal_type = np.random.choice(
            ['BUY', 'SELL', 'HOLD'],
            p=[0.3, 0.3, 0.4]
        )

        return {
            'type': signal_type,
            'price': ticker['price'],
            'timestamp': datetime.now()
        }

    def generate_order(self, signal: Dict) -> Optional[Order]:
        """根据信号生成订单"""
        if signal['type'] == 'HOLD':
            return None

        if signal['type'] == 'BUY' and not self.position:
            return Order(
                symbol=self.config.SYMBOL,
                side=TRADE_SIDES['BUY'],
                order_type=ORDER_TYPES['MARKET'],
                size=Decimal(str(DEFAULT_TRADE_SIZE))
            )

        if signal['type'] == 'SELL' and self.position:
            return Order(
                symbol=self.config.SYMBOL,
                side=TRADE_SIDES['SELL'],
                order_type=ORDER_TYPES['MARKET'],
                size=self.position.size
            )

        return None

    def should_stop_loss(self) -> bool:
        """检查是否触发止损"""
        if not self.position:
            return False

        ticker = self.client.get_ticker(self.config.SYMBOL)
        if not ticker:
            return False

        price_change = calculate_price_change(
            ticker['price'],
            self.position.entry_price
        )

        return price_change <= -self.config.STOP_LOSS_PCT
