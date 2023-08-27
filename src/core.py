from src.utils.utils import ACCOUNTS_LIST
from src.config import *
from src.client.client import Client
from src.defi.jediswap import JediSwap
from src.defi.avnuswap import AvnuSwap
from src.defi.starknetid import StarknetID
from src.defi.dmail import Dmail
from src.okx.okx import withdraw
from src.logger import logger
from asyncio import (sleep, create_task, gather)
from random import randint, shuffle


async def _prepare_account(index, wallet_data: str):
    try:
        address, private = wallet_data.split(':')
        address = int(address, 16)
        client = Client(address=address, private_key=int(private, 16))
        JediSwap_client = JediSwap(client=client)
        Dmail_client = Dmail(client=client)
        AvnuSwap_client = AvnuSwap(client=client)
        StarknetID_client = StarknetID(client=client)

        ROUTERS_TASKS = []
        DMAIL_TX_QUANTITY = 0
        JEDISWAP_SWAP_TX_QUANTITY = 0
        JEDISWAP_POOL_TX_QUANTITY = 0
        AVNUSWAP_TX_QUANTITY = 0
        STARKNETID_TX_QUANTITY = 0

        if ENABLIE_DMAIL:
            DMAIL_TX_QUANTITY = randint(DMAIL_TX_COUNT[0], DMAIL_TX_COUNT[1])
            for _ in range(DMAIL_TX_QUANTITY):
                ROUTERS_TASKS.append(Dmail_client.send_message)

        if ENABLE_JEDISWAP:
            JEDISWAP_SWAP_TX_QUANTITY = randint(JEDISWAP_SWAP_TX_COUNT[0], JEDISWAP_SWAP_TX_COUNT[1])
            for _ in range(JEDISWAP_SWAP_TX_QUANTITY):
                ROUTERS_TASKS.append(JediSwap_client.swap)
            JEDISWAP_POOL_TX_QUANTITY = randint(JEDISWAP_POOL_TX_COUNT[0], JEDISWAP_POOL_TX_COUNT[1])
            for _ in range(JEDISWAP_POOL_TX_QUANTITY):
                ROUTERS_TASKS.append(JediSwap_client.add_liquidity)

        if ENABLE_AVNUSWAP:
            AVNUSWAP_TX_QUANTITY = randint(AVNUSWAP_SWAP_TX_COUNT[0], AVNUSWAP_SWAP_TX_COUNT[1])
            for _ in range(AVNUSWAP_TX_QUANTITY):
                ROUTERS_TASKS.append(AvnuSwap_client.swap)

        if ENABLE_STARKNETID_MINT:
            STARKNETID_TX_QUANTITY = randint(STARKNETID_TX_COUNT[0], STARKNETID_TX_COUNT[1])
            for _ in range(STARKNETID_TX_QUANTITY):
                ROUTERS_TASKS.append(StarknetID_client.mint)

        shuffle(ROUTERS_TASKS)
        total_tasks_quantity = len(ROUTERS_TASKS)
        logger.info(f"[{address}] [{index}] | Loaded {total_tasks_quantity} tasks.")
        logger.info(f"\tDmail: {DMAIL_TX_QUANTITY} | StarknetID: {STARKNETID_TX_QUANTITY}")
        logger.info(f"\tJediSwap swaps: {JEDISWAP_SWAP_TX_QUANTITY} | JediSwap pool: {JEDISWAP_POOL_TX_QUANTITY}")
        logger.info(f"\tAvnuSwap swaps: {AVNUSWAP_TX_QUANTITY}")

        if ENABLE_WITHDRAW_FROM_OKX:
            delay = randint(DELAY_BEFORE_WITHDRAW[0], DELAY_BEFORE_WITHDRAW[1])
            logger.info(f"[{address}] [{index}] | Sleeping for {delay} sec before withdrawing from OKX")
            await sleep(delay)
            if await withdraw(wallet=wallet_data.split(':')[0]):
                delay = randint(DELAY_AFTER_WITHDRAW[0], DELAY_AFTER_WITHDRAW[1])
                logger.info(f"[{address}] [{index}] | Sleeping for {delay} sec after withdrawing from OKX")
                await sleep(delay)
            else:
                logger.warning(f"[{address}] [{index}] | Stopped work because couldn't withdraw from OKX")
                with open('non-withdrew-wallets.txt', 'a+') as file:
                    file.writelines(f"{wallet_data}\n")
                return

        initial_delay = randint(INITIAL_DELAY[0], INITIAL_DELAY[1])
        logger.info(f"[{address}] [{index}] | Sleeping for {initial_delay} seconds before working")
        await sleep(initial_delay)

        for index_task, task in enumerate(ROUTERS_TASKS):
            try:
                eth_Balance = (await client.get_balance()).Ether
                if eth_Balance >= 0.000060606:
                    for attempt in range(5):
                        logger.info(f"[{address}] [{index}] | Making {index_task + 1} task | Attempt {attempt + 1 }/5... ")
                        if await task():
                            logger.success(f"[{address}] [{index}] | Made {index_task + 1} task ")
                            delay = randint(DELAY_BETWEEN_ACTIONS[0], DELAY_BETWEEN_ACTIONS[1])
                            logger.info(f"[{address}] [{index}] | Sleeping for {delay} sec before next task... ")
                            await sleep(delay)
                            break
                else:
                    logger.warning(f"[{address}] [{index}] | ETH Balance: {eth_Balance}... Stopped the work")
                    break
            except Exception as exc:
                logger.error(f"[{address}] [{index}] | Unexpected error while making {index + 1} task... {exc}")

        with open('ended.txt', 'a+') as file:
            file.writelines(f"{wallet_data}\n")
    except Exception as exc:
        logger.critical(f"Unexpected error: {wallet_data} | {exc}. Work is ended! ")


async def prepare_accounts():
    all_tasks = []
    logger.info(f"Loaded {len(ACCOUNTS_LIST)} accounts")
    for index, account in enumerate(ACCOUNTS_LIST):
        all_tasks.append(create_task(_prepare_account(wallet_data=account, index=index + 1)))
        await sleep(3)
    return all_tasks


async def start():
    if not NODE_URL:
        logger.critical(f"There is no NODE_URL in config. Replace it with your node")
        return
    await gather(* await prepare_accounts())
