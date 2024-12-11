"""交易系统配置设置"""
import os
from src.utils.env_loader import load_env_vars


class Config:
    def __init__(self):
        # 加载环境变量
        env_vars = load_env_vars()

        # API配置
        self.API_KEY = env_vars.get('API_KEY')
        self.API_SECRET = env_vars.get('API_SECRET')
        self.API_PASSPHRASE = env_vars.get('API_PASSPHRASE')
        self.IS_TESTNET = env_vars.get('IS_TESTNET', 'True').lower() == 'true'

        # 交易参数
        self.SYMBOL = 'BTC-USDT'
        self.TRADE_SIZE = 0.001
        self.STOP_LOSS_PCT = 0.02
        self.MIN_CONFIDENCE = 0.7
        self.TRADING_INTERVAL = 60  # 秒

        # 验证配置
        self._validate_config()

    def _validate_config(self):
        """验证配置参数"""
        if not all([self.API_KEY, self.API_SECRET, self.API_PASSPHRASE]):
            raise ValueError("API配置不完整")
