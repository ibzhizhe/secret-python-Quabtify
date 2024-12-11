"""交易引擎核心模块"""
import time
from src.client.okx_client import OKXClient
from src.strategy.simple_strategy import SimpleStrategy
from src.utils.logger import get_logger


class TradingEngine:
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        self.client = OKXClient(config)
        self.strategy = SimpleStrategy(self.client, config)
        self.is_running = False

        self.logger.info(f"交易模式: {'测试' if config.IS_TESTNET else '实盘'}")
        self.logger.info(f"交易对: {config.SYMBOL}")

    def start(self):
        """启动交易引擎"""
        self.is_running = True
        self._run_trading_loop()

    def stop(self):
        """停止交易引擎"""
        self.is_running = False
        self.logger.info("交易引擎已停止")

    def _run_trading_loop(self):
        """运行交易主循环"""
        while self.is_running:
            try:
                self._process_trading_cycle()
                time.sleep(self.config.TRADING_INTERVAL)
            except Exception as e:
                self.logger.error(f"交易循环错误: {str(e)}")

    def _process_trading_cycle(self):
        """处理单个交易周期"""
        # 获取账户信息
        balance = self.client.get_account_balance()
        self.logger.info(f"当前余额: {balance}")

        # 检查止损条件
        if self.strategy.should_stop_loss():
            self.logger.warning("触发止损条件")
            self.strategy.execute_stop_loss()
            return

        # 获取并执行交易信号
        signal = self.strategy.analyze_market()
        if signal and signal.confidence >= self.config.MIN_CONFIDENCE:
            self.logger.info(f"生成信号: {signal}")
            result = self.strategy.execute_trade(signal)
            if result:
                self.logger.info(f"交易执行结果: {result}")
