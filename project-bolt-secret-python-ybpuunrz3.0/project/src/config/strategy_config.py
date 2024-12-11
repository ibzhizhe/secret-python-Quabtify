"""策略配置"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class StrategyConfig:
    """策略配置类"""
    SYMBOL: str = "BTC-USDT"  # 交易对
    CONTRACT_TYPE: str = "SWAP"  # 合约类型(永续)
    POSITION_MODE: str = "one-way"  # 持仓模式(单向)
    LEVERAGE: int = 100  # 杠杆倍数
    TRADE_SIZE: Decimal = Decimal('0.001')  # 交易数量

    # 技术指标参数
    EMA_FAST_PERIOD: int = 12  # 快速EMA周期
    EMA_SLOW_PERIOD: int = 144  # 慢速EMA周期

    # 风控参数
    MAX_POSITIONS: int = 1  # 最大持仓数
    STOP_LOSS_PCT: float = 0.02  # 止损比例
    TAKE_PROFIT_PCT: float = 0.04  # 止盈比例
