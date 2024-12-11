"""OKX API客户端"""
from decimal import Decimal
from typing import Dict, Optional, List
import okx.MarketData as Market
import okx.Trade as Trade
import okx.Account as Account
from src.models.market_data import MarketData
from src.models.order import Order
from src.utils.error_handler import handle_api_error


class OKXClient:
    def __init__(self, config):
        self.config = config
        self._init_api_clients()
        self._setup_trading_config()

    def _init_api_clients(self):
        """初始化API客户端"""
        api_params = {
            'api_key': self.config.API_KEY,
            'api_secret_key': self.config.API_SECRET,
            'passphrase': self.config.API_PASSPHRASE,
            'flag': "1" if self.config.IS_TESTNET else "0"
        }

        self.market = Market.MarketAPI(**api_params)
        self.trade = Trade.TradeAPI(**api_params)
        self.account = Account.AccountAPI(**api_params)

    def _setup_trading_config(self):
        """设置交易配置"""
        # 设置持仓模式
        self.account.set_position_mode(
            posMode=self.config.POSITION_MODE,
            instId=self.config.SYMBOL
        )

        # 设置杠杆倍数
        self.account.set_leverage(
            lever=str(self.config.LEVERAGE),
            mgnMode='cross',  # 全仓模式
            instId=self.config.SYMBOL
        )

    @handle_api_error
    def get_market_data(self, symbol: str) -> Optional[MarketData]:
        """获取市场数据"""
        response = self.market.get_ticker(instId=symbol)
        if not response or 'data' not in response:
            return None

        data = response['data'][0]
        return MarketData(
            symbol=symbol,
            price=Decimal(data['last']),
            volume=Decimal(data.get('vol24h', '0')),
            high_24h=Decimal(data.get('high24h', '0')),
            low_24h=Decimal(data.get('low24h', '0'))
        )

    @handle_api_error
    def get_kline_data(self, symbol: str, period: str = '1m', limit: int = 300) -> List[Dict]:
        """获取K线数据"""
        response = self.market.get_candlesticks(
            instId=symbol,
            bar=period,
            limit=str(limit)
        )
        return response.get('data', [])

    @handle_api_error
    def place_order(self, order: Order) -> Dict:
        """下单"""
        order_data = order.to_dict()
        response = self.trade.place_order(**order_data)
        return self._parse_order_response(response)

    def _parse_order_response(self, response: Dict) -> Dict:
        """解析订单响应"""
        if not response or 'data' not in response:
            return {}

        data = response['data'][0]
        return {
            'order_id': data.get('ordId'),
            'status': data.get('state'),
            'message': data.get('sMsg', '')
        }
