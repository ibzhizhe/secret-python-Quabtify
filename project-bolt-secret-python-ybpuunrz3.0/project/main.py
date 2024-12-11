"""交易系统主入口"""
import time
import logging
from src.client.okx_client import OKXClient
from src.strategy.simple_strategy import SimpleStrategy
from src.config.config import Config
from src.utils.error_handler import TradingError


def setup_logging():
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def main():
    """主程序入口"""
    logger = setup_logging()
    logger.info("启动 OKX 交易系统...")

    try:
        # 初始化组件
        client = OKXClient(Config())
        strategy = SimpleStrategy(client, Config())

        logger.info(f"交易模式: {'测试网' if Config.IS_TESTNET else '主网'}")
        logger.info(f"交易对: {Config.SYMBOL}")

        # 主交易循环
        while True:
            try:
                # 获取账户信息
                balance = client.get_account_balance()
                logger.info(f"账户余额: {balance}")

                # 检查止损
                if strategy.should_stop_loss():
                    logger.warning("触发止损条件")
                    signal = {'type': 'SELL', 'price': None}
                else:
                    # 分析市场获取信号
                    signal = strategy.analyze_market()

                if signal:
                    logger.info(f"交易信号: {signal}")
                    # 生成订单
                    order = strategy.generate_order(signal)
                    if order:
                        # 执行交易
                        result = client.place_order(order)
                        logger.info(f"订单结果: {result}")

                time.sleep(Config.TRADING_INTERVAL)

            except TradingError as e:
                logger.error(f"交易错误: {str(e)}")
                time.sleep(5)  # 错误后短暂等待

    except KeyboardInterrupt:
        logger.info("用户停止交易系统")
    except Exception as e:
        logger.error(f"系统错误: {str(e)}")
        raise


if __name__ == "__main__":
    main()
