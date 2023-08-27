import ccxt
from src.config import OKX_PASSWORD_FROM_KEY, OKX_API_KEY, OKX_SECRET_KEY, ETH_TO_WITHDRAW, PROXY_FOR_OKX
from random import uniform
from loguru import logger


async def withdraw(wallet):
    try:
        logger.debug(f"[{wallet}] Withdrawing for: {wallet}")
        amount = round(uniform(ETH_TO_WITHDRAW[0], ETH_TO_WITHDRAW[1]), 5)
        params = {
            'apiKey': OKX_API_KEY,
            'secret': OKX_SECRET_KEY,
            'password': OKX_PASSWORD_FROM_KEY,
            'enableRateLimit': True,
        }
        if PROXY_FOR_OKX:
            params['proxies'] = PROXY_FOR_OKX
        exchange = ccxt.okx(params)
        withdraw = exchange.withdraw('ETH', amount, wallet,
                                     params={
                    "toAddress": wallet,
                    "chainName": 'StarkNet',
                    "dest": 4,
                    "pwd": '-',
                    "amt": amount,
                    "network": 'StarkNet'
                })
        if withdraw.get('info'):
            logger.success(f"[{wallet}] Withdrew {amount} ETH")
            return True
    except Exception as exc:
        logger.error(f"[{wallet}] Couldn't withdraw ETH | {exc}")
