"""交易系统常量定义"""

# 交易相关常量
TRADE_MODES = {
    'CASH': 'cash',      # 现货交易
    'MARGIN': 'margin',  # 杠杆交易
    'ISOLATED': 'isolated'  # 逐仓交易
}

ORDER_TYPES = {
    'MARKET': 'market',  # 市价单
    'LIMIT': 'limit'     # 限价单
}

TRADE_SIDES = {
    'BUY': 'buy',   # 买入
    'SELL': 'sell'  # 卖出
}

# 时间常量
DEFAULT_TRADING_INTERVAL = 60  # 默认交易间隔(秒)
MARKET_DATA_TIMEOUT = 30      # 市场数据超时时间(秒)

# 交易参数默认值
DEFAULT_TRADE_SIZE = 0.001     # 默认交易数量
DEFAULT_STOP_LOSS_PCT = 0.02   # 默认止损比例
DEFAULT_TAKE_PROFIT_PCT = 0.03 # 默认止盈比例