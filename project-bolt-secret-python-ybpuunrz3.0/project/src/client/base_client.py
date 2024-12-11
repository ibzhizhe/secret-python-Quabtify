"""基础API客户端"""
import okx.Account as Account
import okx.MarketData as Market
import okx.Trade as Trade


class BaseClient:
    def __init__(self, config):
        self.config = config
        self.flag = "1" if config.IS_TESTNET else "0"

    def _init_api_clients(self):
        """初始化API客户端"""
        api_params = {
            'api_key': self.config.API_KEY,
            'api_secret_key': self.config.API_SECRET,
            'passphrase': self.config.API_PASSPHRASE,
            'flag': self.flag
        }

        self.account = Account.AccountAPI(**api_params)
        self.market = Market.MarketAPI(**api_params)
        self.trade = Trade.TradeAPI(**api_params)
