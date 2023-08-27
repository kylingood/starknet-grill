from src.client.client import Client
from src.utils.scripts import get_data_for_swap
from src.models.models import TokenAmount, DefaultContractData
from src.config import SLIPPAGE
from src.logger import logger
from starknet_py.contract import Contract
from random import choice


class AvnuSwap:

    AVNUSWAP_CONTRACT = DefaultContractData.AVNUSWAP_CONTRACT.get('address')
    AVNUSWAP_ABI = DefaultContractData.AVNUSWAP_CONTRACT.get('abi')


    def __init__(self, client: Client):
        self.client = client
        self.contract = Contract(address=AvnuSwap.AVNUSWAP_CONTRACT, abi=AvnuSwap.AVNUSWAP_ABI, provider=self.client.account)

    async def swap(self, swap_to_eth = False, data_for_swap = None) -> bool:
        try:
            ROUTERS_ADDRESSES_LIST = [DefaultContractData.JEDISWAP_CONTRACT.get('address')]
            if not data_for_swap:
                data_for_swap = await get_data_for_swap(client=self.client, swap_to_eth=swap_to_eth)
            if data_for_swap == {}:
                return False
            amount, to_token_address, to_token_name, from_token_address, from_token_name, from_token_decimals = data_for_swap.values()

            logger.debug(
                f"[{self.client.address}] Swapping {amount.Ether} {from_token_name} to {to_token_name}...[AvnuSwap]")
            is_approved = await self.client.approve_interface(token_address=from_token_address,
                                                              spender=AvnuSwap.AVNUSWAP_CONTRACT,
                                                              decimals=from_token_decimals, amount=amount)
            if is_approved:
                eth_price = self.client.get_eth_price(token='ETH')
                if to_token_name == 'USDT' or to_token_name == 'USDC':
                    if from_token_name == 'ETH':
                        min_to_amount = TokenAmount(amount=eth_price * float(amount.Ether) * (1 - SLIPPAGE / 100),
                                                    decimals=6)
                    elif from_token_name == 'DAI':
                        min_to_amount = TokenAmount(amount=float(amount.Ether) * (1 - SLIPPAGE / 100),
                                                    decimals=6)
                elif to_token_name == 'ETH':
                    min_to_amount = TokenAmount(amount=float(amount.Ether) / eth_price * (1 - SLIPPAGE / 100),
                                                decimals=18)
                elif to_token_name == 'DAI':
                    if from_token_name == 'USDT' or from_token_name == 'USDC':
                        min_to_amount = TokenAmount(amount=float(amount.Ether) * (1 - SLIPPAGE / 100), decimals=18)
                    elif from_token_name == 'ETH':
                        min_to_amount = TokenAmount(amount=eth_price * float(amount.Ether) * (1 - SLIPPAGE / 100),
                                                    decimals=18)
                tx_hash = await self.client.call(interacted_contract_address=AvnuSwap.AVNUSWAP_CONTRACT,
                                                 calldata=[
                                                     from_token_address,
                                                     amount.Wei,
                                                     0,
                                                     to_token_address,
                                                     min_to_amount.Wei,
                                                     0,
                                                     min_to_amount.Wei,
                                                     0,
                                                     self.client.address,
                                                     0,
                                                     0,
                                                     1,
                                                     from_token_address,
                                                     to_token_address,
                                                     choice(ROUTERS_ADDRESSES_LIST),
                                                     0x64
                                                 ],
                                                 selector_name='multi_route_swap')
                if tx_hash:
                    logger.success(
                        f"[{self.client.address}] Successfully swapped {amount.Ether} {from_token_name} to {min_to_amount.Ether} {to_token_name} | [AvnuSwap]")
                    return True
        except Exception as exc:
            logger.error(f"[{self.client.address}] Couldn't swap | [AvnuSwap] | {exc}")
