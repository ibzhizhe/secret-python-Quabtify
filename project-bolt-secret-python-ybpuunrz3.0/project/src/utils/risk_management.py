"""风险管理工具"""
from decimal import Decimal
from typing import Optional
from src.models.position import Position

def calculate_position_risk(
    position: Position,
    current_price: Decimal,
    account_balance: Decimal
) -> float:
    """计算持仓风险度"""
    position_value = position.size * current_price
    return float(position_value / account_balance)

def calculate_optimal_position_size(
    account_balance: Decimal,
    risk_per_trade: float,
    stop_loss_pct: float
) -> Decimal:
    """计算最优仓位大小"""
    risk_amount = account_balance * Decimal(str(risk_per_trade))
    return risk_amount / Decimal(str(stop_loss_pct))

def calculate_stop_loss_price(
    entry_price: Decimal,
    side: str,
    stop_loss_pct: float
) -> Decimal:
    """计算止损价格"""
    stop_loss_decimal = Decimal(str(stop_loss_pct))
    if side == 'long':
        return entry_price * (1 - stop_loss_decimal)
    return entry_price * (1 + stop_loss_decimal)

def calculate_take_profit_price(
    entry_price: Decimal,
    side: str,
    risk_reward_ratio: float
) -> Decimal:
    """计算止盈价格"""
    if side == 'long':
        return entry_price * (1 + Decimal(str(risk_reward_ratio)))
    return entry_price * (1 - Decimal(str(risk_reward_ratio)))