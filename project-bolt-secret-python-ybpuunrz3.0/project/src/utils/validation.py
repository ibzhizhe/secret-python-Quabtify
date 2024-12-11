"""参数验证工具"""
from decimal import Decimal
from typing import Union, Dict, Optional
from src.constants.trading_constants import TRADE_SIDES, ORDER_TYPES

def validate_symbol(symbol: str) -> bool:
    """验证交易对格式"""
    if not isinstance(symbol, str):
        return False
    parts = symbol.split('-')
    return len(parts) == 2 and all(parts)

def validate_order_params(
    symbol: str,
    side: str,
    size: Union[float, Decimal],
    order_type: str,
    price: Optional[Union[float, Decimal]] = None
) -> Dict[str, str]:
    """验证订单参数"""
    errors = {}
    
    if not validate_symbol(symbol):
        errors['symbol'] = '无效的交易对格式'
    
    if side not in TRADE_SIDES.values():
        errors['side'] = '无效的交易方向'
    
    if not isinstance(size, (float, Decimal)) or size <= 0:
        errors['size'] = '无效的交易数量'
    
    if order_type not in ORDER_TYPES.values():
        errors['order_type'] = '无效的订单类型'
    
    if order_type == ORDER_TYPES['LIMIT']:
        if not price or not isinstance(price, (float, Decimal)) or price <= 0:
            errors['price'] = '限价单必须指定有效价格'
    
    return errors

def validate_position_params(
    symbol: str,
    side: str,
    size: Union[float, Decimal],
    entry_price: Union[float, Decimal],
    stop_loss: Optional[Union[float, Decimal]] = None,
    take_profit: Optional[Union[float, Decimal]] = None
) -> Dict[str, str]:
    """验证持仓参数"""
    errors = {}
    
    if not validate_symbol(symbol):
        errors['symbol'] = '无效的交易对格式'
    
    if side not in ['long', 'short']:
        errors['side'] = '无效的持仓方向'
    
    if not isinstance(size, (float, Decimal)) or size <= 0:
        errors['size'] = '无效的持仓数量'
    
    if not isinstance(entry_price, (float, Decimal)) or entry_price <= 0:
        errors['entry_price'] = '无效的开仓价格'
    
    if stop_loss is not None:
        if not isinstance(stop_loss, (float, Decimal)) or stop_loss <= 0:
            errors['stop_loss'] = '无效的止损价格'
    
    if take_profit is not None:
        if not isinstance(take_profit, (float, Decimal)) or take_profit <= 0:
            errors['take_profit'] = '无效的止盈价格'
    
    return errors