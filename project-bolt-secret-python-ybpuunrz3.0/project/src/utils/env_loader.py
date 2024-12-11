"""环境变量加载工具"""
import os
from dotenv import load_dotenv


def load_env_vars():
    """加载并返回环境变量"""
    load_dotenv()

    return {
        'API_KEY': os.getenv('API_KEY'),
        'API_SECRET': os.getenv('API_SECRET'),
        'API_PASSPHRASE': os.getenv('API_PASSPHRASE'),
        'IS_TESTNET': os.getenv('IS_TESTNET', 'True')
    }
