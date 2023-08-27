import asyncio
import requests

from src.config import NODE_URL, MAX_GWEI, RANDOM_INCREASE_FEE, USE_PROXY
from src.models.models import TokenAmount, DefaultContractData
from src.utils.utils import PROXY_ITER
from src.logger import logger
from typing import Optional
from random import randint, uniform
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.contract import Contract, PreparedFunctionCall
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector


class Client:

    def __init__(self, address, private_key):
        if not USE_PROXY:
            self.full_node_client = FullNodeClient(node_url=NODE_URL)
        else:
            self._PROXY = next(PROXY_ITER)
            self._TCP_CONNECTOR = ProxyConnector.from_url(self._PROXY)
            self.full_node_client = FullNodeClient(node_url=NODE_URL, session=ClientSession(connector=self._TCP_CONNECTOR))
        self.address = address
        self.private_key = private_key
        self.account = Account(client=self.full_node_client,
                               address=self.address,
                               key_pair=KeyPair.from_private_key(self.private_key),
                               chain=StarknetChainId.MAINNET)
        self._last_prepared_tx = None

    async def estimate_fee(self, prepared_tx: PreparedFunctionCall = None):
        async def _response():
            nonlocal prepared_tx
            if not prepared_tx:
                prepared_tx = self._last_prepared_tx
            response = await prepared_tx.estimate_fee()
            overall_fee = response.overall_fee
            gas_price = response.gas_price / 10 ** 9
            self._last_prepared_tx = prepared_tx
            return {'gas_price': gas_price, 'overall_fee': overall_fee}

        response = await _response()
        gas_price = response.get('gas_price')
        while gas_price >= MAX_GWEI:
            logger.warning(f"Current gas price: {gas_price} GWEI. Waiting to dump...")
            try:
                response = await _response()
                gas_price = response.get('gas_price')
            except Exception as exc:
                logger.error(exc)
            await asyncio.sleep(randint(60, 120))
        overall_fee = response.get('overall_fee')
        return overall_fee

    async def _approve(self, token_address, spender, amount) -> bool:
        data = DefaultContractData.get_data_from_contract(contract=token_address)
        abi = data.get('abi')
        name = data.get('name')
        logger.debug(f"[{self.address}] Approving {name}...")
        contract = Contract(address=token_address, abi=abi,
                            provider=self.account)
        prepared_tx = contract.functions['approve'].prepare(spender=spender,
                                                            amount=amount)
        fee = await self.estimate_fee(prepared_tx=prepared_tx)
        tx = await prepared_tx.invoke(max_fee=int(fee * (1 + randint(RANDOM_INCREASE_FEE[0], RANDOM_INCREASE_FEE[1]) / 100)))
        for _ in range(150):
            try:
                receipt = await self.account.client.get_transaction_receipt(tx.hash)
                block = receipt.block_number
                if block:
                    return True
            except:
                pass
            finally:
                await asyncio.sleep(2.5)

    async def approve_interface(self, token_address, spender, decimals, amount: Optional[TokenAmount] = None) -> bool:
        name = DefaultContractData.get_data_from_contract(contract=token_address).get('name')
        balance = await self.get_balance(token_address=token_address, decimals=decimals)
        if balance.Wei <= 0:
            logger.error(f"[{self.address}] Zero balance for {name}")
            return False

        if not amount or amount.Wei > balance.Wei:
            amount = balance
        approved_amount = await self.get_allowance(token_address=token_address, spender=spender)
        if approved_amount.Wei >= amount.Wei:
            logger.debug(f"[{self.address}] Already approved {approved_amount.Ether} {name}")
            return True
        approved_tx = await self._approve(token_address=token_address, amount=amount.Wei, spender=spender)
        if approved_tx:
            logger.debug(f"[{self.address}] Approved {amount.Ether} {name}")
            random_sleep = randint(180, 250)
            logger.info(f"[{self.address}] SLeeping for {random_sleep} sec before sending tx...")
            await asyncio.sleep(random_sleep)
            return True
        return False

    async def get_allowance(self, token_address, spender) -> Optional[TokenAmount]:
        data = DefaultContractData.get_data_from_contract(contract=token_address)
        abi = data.get('abi')
        decimals = data.get('decimals')
        contract = Contract(address=token_address, abi=abi,
                            provider=self.account)
        allowance_check = await contract.functions['allowance'].prepare(owner=self.address,
                                                                        spender=spender).call()
        if token_address == 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3:
            amount = allowance_check.res
        else:
            amount = allowance_check.remaining
        return TokenAmount(amount=amount, decimals=decimals, wei=True)

    async def call(self, interacted_contract_address, calldata, selector_name):
        try:
            logger.debug(f"[{self.address}] Sending tx...")
            call = Call(to_addr=interacted_contract_address, selector=get_selector_from_name(selector_name),
                        calldata=calldata)
            max_fee = TokenAmount(amount=float(uniform(0.0007534534534, 0.001)))
            await self.estimate_fee()
            resp = await self.account.execute(calls=[call], max_fee=int(max_fee.Wei * (1 + randint(RANDOM_INCREASE_FEE[0], RANDOM_INCREASE_FEE[1]) / 100)))
            for _ in range(150):
                try:
                    receipt = await self.account.client.get_transaction_receipt(resp.transaction_hash)
                    block = receipt.block_number
                    if block:
                        return True
                except:
                    pass
                finally:
                    await asyncio.sleep(2.5)
        except Exception as exc:
            logger.error(f"Couldn't send tx: {exc}")

    async def send_transaction(self, interacted_contract, function_name=None, **kwargs) -> bool:
        try:
            logger.debug(f"[{self.address}] Sending tx...")

            prepared_tx = interacted_contract.functions[function_name].prepare(**kwargs)
            fee = await self.estimate_fee(prepared_tx)
            tx = await prepared_tx.invoke(max_fee=int(fee * (1 + randint(RANDOM_INCREASE_FEE[0], RANDOM_INCREASE_FEE[1]) / 100)))
            for _ in range(150):
                try:
                    receipt = await self.account.client.get_transaction_receipt(tx.hash)
                    block = receipt.block_number
                    if block:
                        return True
                except Exception as exc:
                    pass
                finally:
                    await asyncio.sleep(2.5)
        except Exception as exc:
            logger.error(f"Couldn't send tx: {exc}")

    async def get_balance(self, token_address = 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7, decimals=18) -> TokenAmount:
        balance = await self.account.get_balance(token_address=token_address)
        return TokenAmount(amount=balance, wei=True, decimals=decimals)

    def get_eth_price(self, token='ETH'):
        token = token.upper()
        logger.info(f'[{self.address}] | Getting {token} price')
        response = requests.get(f'https://api.binance.com/api/v3/depth?limit=1&symbol={token}USDT')
        if response.status_code != 200:
            logger.warning(f'code: {response.status_code} | json: {response.json()}')
            return
        result_dict = response.json()
        if 'asks' not in result_dict:
            logger.warning(f'code: {response.status_code} | json: {response.json()}')
            return
        return float(result_dict['asks'][0][0])
