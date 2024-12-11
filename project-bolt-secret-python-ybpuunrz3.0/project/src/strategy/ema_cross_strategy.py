"""EMA交叉策略实现"""
from decimal import Decimal
from typing import List, Optional
from datetime import datetime
from src.models.trade_signal import TradeSignal
from src.models.market_data import MarketData
from src.models.position import Position
from src.utils.market_utils import calculate_moving_average


class EMACrossStrategy:
    def __init__(self, client, config):
        """初始化策略"""
        self.client = client
        self.config = config
        self.position: Optional[Position] = None
        self.price_history: List[Decimal] = []
        self.ema12_history: List[Decimal] = []
        self.ema144_history: List[Decimal] = []

    def calculate_ema(self, prices: List[Decimal], period: int, smoothing: float = 2.0) -> List[Decimal]:
        """计算EMA"""
        ema = []
        if len(prices) < period:
            return ema

        # 初始化EMA为前N个价格的简单平均值
        sma = sum(prices[:period]) / period
        multiplier = smoothing / (1 + period)
        ema.append(sma)

        # 计算后续的EMA值
        for price in prices[period:]:
            ema_value = (price * multiplier) + (ema[-1] * (1 - multiplier))
            ema.append(ema_value)

        return ema

    def update_indicators(self, market_data: MarketData) -> None:
        """更新技术指标"""
        self.price_history.append(market_data.price)

        # 保持价格历史在最大所需周期内
        max_period = 144
        if len(self.price_history) > max_period * 2:
            self.price_history = self.price_history[-max_period * 2:]

        # 计算EMA
        if len(self.price_history) >= 144:
            self.ema12_history = self.calculate_ema(self.price_history, 12)
            self.ema144_history = self.calculate_ema(self.price_history, 144)

    def check_cross_signals(self) -> Optional[str]:
        """检查EMA交叉信号"""
        if len(self.ema12_history) < 2 or len(self.ema144_history) < 2:
            return None

        # 检查EMA12上穿EMA144
        if (self.ema12_history[-2] <= self.ema144_history[-2] and
                self.ema12_history[-1] > self.ema144_history[-1]):
            return 'LONG'

        # 检查EMA12下穿EMA144
        if (self.ema12_history[-2] >= self.ema144_history[-2] and
                self.ema12_history[-1] < self.ema144_history[-1]):
            return 'SHORT'

        return None

    def analyze_market(self) -> Optional[TradeSignal]:
        """分析市场生成交易信号"""
        market_data = self.client.get_market_data(self.config.SYMBOL)
        if not market_data:
            return None

        self.update_indicators(market_data)
        cross_signal = self.check_cross_signals()

        if not cross_signal:
            return None

        # 生成交易信号
        if cross_signal == 'LONG':
            if self.position and self.position.side == 'short':
                # 先平空
                return TradeSignal(
                    signal_type='SELL',
                    price=market_data.price,
                    timestamp=datetime.now(),
                    confidence=1.0,
                    reason="EMA12上穿EMA144,平空"
                )
            elif not self.position:
                # 开多
                return TradeSignal(
                    signal_type='BUY',
                    price=market_data.price,
                    timestamp=datetime.now(),
                    confidence=1.0,
                    reason="EMA12上穿EMA144,开多"
                )

        elif cross_signal == 'SHORT':
            if self.position and self.position.side == 'long':
                # 先平多
                return TradeSignal(
                    signal_type='SELL',
                    price=market_data.price,
                    timestamp=datetime.now(),
                    confidence=1.0,
                    reason="EMA12下穿EMA144,平多"
                )
            elif not self.position:
                # 开空
                return TradeSignal(
                    signal_type='BUY',
                    price=market_data.price,
                    timestamp=datetime.now(),
                    confidence=1.0,
                    reason="EMA12下穿EMA144,开空"
                )

        return None
