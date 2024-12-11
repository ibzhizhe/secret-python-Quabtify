"""市场数据工具"""
from decimal import Decimal
from typing import Dict, Optional
from datetime import datetime
from src.models.market_data import MarketData

def calculate_price_change(
    current_price: Decimal,
    reference_price: Decimal
) -> Decimal:
    """计算价格变化百分比"""
    if reference_price == 0:
        return Decimal('0')
    return ((current_price - reference_price) / reference_price) * 100

def parse_ticker_data(ticker_response: Dict) -> Optional[MarketData]:
    """解析行情数据"""
    try:
        if not ticker_response or 'data' not in ticker_response:
            return None
            
        data = ticker_response['data'][0]
        return MarketData(
            symbol=data['instId'],
            price=Decimal(data['last']),
            timestamp=datetime.now(),
            volume=Decimal(data.get('vol24h', '0')),
            high_24h=Decimal(data.get('high24h', '0')),
            low_24h=Decimal(data.get('low24h', '0')),
            open_24h=Decimal(data.get('open24h', '0')),
            close_24h=Decimal(data.get('last', '0'))
        )
    except (KeyError, ValueError, IndexError):
        return None

def calculate_moving_average(prices: list[Decimal], period: int) -> Optional[Decimal]:
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period