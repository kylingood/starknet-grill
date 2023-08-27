from src.client.client import Client
from src.models.models import DefaultContractData, TokenAmount
from src.logger import logger
from src.config import PERCENTAGE_BALANCE_FOR_SWAP
from random import choice, uniform, shuffle


async def _get_data_for_swap(client: Client, swap_to_eth = False) -> dict:
    try:
        ETH_ADDRESS = DefaultContractData.ETH_CONTRACT.get('address')
        USDT_ADDRESS = DefaultContractData.USDT_CONTRACT.get('address')
        USDC_ADDRESS = DefaultContractData.USDC_CONTRACT.get('address')
        DAI_ADDRESS = DefaultContractData.DAI_CONTRACT.get('address')
        tokens_list = [ETH_ADDRESS, USDC_ADDRESS, USDT_ADDRESS, DAI_ADDRESS]
        shuffle(tokens_list)
        to_token = choice(tokens_list)
        to_token_data = DefaultContractData.get_data_from_contract(to_token)
        to_token_name = to_token_data.get('name')
        to_token_address = to_token_data.get('address')
        tokens_list.remove(to_token)

        from_token_data = DefaultContractData.get_data_from_contract(choice(tokens_list))
        from_token_address = from_token_data.get('address')
        from_token_name = from_token_data.get('name')
        from_token_decimals = from_token_data.get('decimals')
        balance_first_token = 0
        amount = TokenAmount(amount=0)

        for from_token_address_ in tokens_list:
            balance_first_token = await client.get_balance(token_address=from_token_address_,
                                                           decimals=DefaultContractData.get_data_from_contract(from_token_address_).get('decimals'))
            if balance_first_token.Wei > 0:
                from_token_address = from_token_address_
                from_token_name = DefaultContractData.get_data_from_contract(from_token_address).get('name')
                from_token_decimals = DefaultContractData.get_data_from_contract(from_token_address).get('decimals')
                break
            else:
                balance_first_token = TokenAmount(amount=0)

        from_amount = float(balance_first_token.Ether) * (PERCENTAGE_BALANCE_FOR_SWAP[0] / 100)
        to_amount = float(balance_first_token.Ether) * (PERCENTAGE_BALANCE_FOR_SWAP[1] / 100)
        amount = TokenAmount(
            amount=round(uniform(from_amount, to_amount), from_token_decimals),
            decimals=from_token_decimals)
        if amount.Ether > 0:
            return {'amount': amount,
                    'to_token_address': to_token_address,
                    'to_token_name': to_token_name,
                    'from_token_address': from_token_address,
                    'from_token_name': from_token_name,
                    'from_token_decimals': from_token_decimals}
    except Exception as exc:
        logger.error(f"[{client.address}] Couldn't get data for swap | {exc}")


async def _get_data_for_liquidity_pool(client: Client, dex_name: str) -> dict:
    try:
        ETH_ADDRESS = DefaultContractData.ETH_CONTRACT.get('address')
        USDT_ADDRESS = DefaultContractData.USDT_CONTRACT.get('address')
        USDC_ADDRESS = DefaultContractData.USDC_CONTRACT.get('address')
        tokens_list = [ETH_ADDRESS, USDC_ADDRESS, USDT_ADDRESS]

        from_token = choice(tokens_list)
        tokens_list.remove(from_token)
        to_token = choice(tokens_list)

        token_one_data = DefaultContractData.get_data_from_contract(from_token)
        token_two_data = DefaultContractData.get_data_from_contract(to_token)

        token_one_address = token_one_data.get('address')
        token_two_address = token_two_data.get('address')

        token_one_decimals = token_one_data.get('decimals')
        token_two_decimals = token_two_data.get('decimals')

        pooled_token_data = {}
        amount_one = 0
        amount_two = 0
        amount_in_usdt = 0

        # ETH/USDT pool
        if (token_one_address == ETH_ADDRESS and token_two_address == USDT_ADDRESS) or (token_one_address == USDT_ADDRESS and token_two_address == ETH_ADDRESS):
            if dex_name == 'jediswap':
                pooled_token_data = DefaultContractData.get_data_from_contract(0x045e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6)
            token_one_name = 'ETH'
            token_one_address = ETH_ADDRESS
            token_one_decimals = 18
            token_two_name = 'USDT'
            token_two_address = USDT_ADDRESS
            token_two_decimals = 6

        elif (token_one_address == ETH_ADDRESS and token_two_address == USDC_ADDRESS) or (token_one_address == USDC_ADDRESS and token_two_address == ETH_ADDRESS):
            if dex_name == 'jediswap':
                pooled_token_data = DefaultContractData.get_data_from_contract(
                    0x04d0390b777b424e43839cd1e744799f3de6c176c7e32c1812a41dbd9c19db6a)

            token_one_name = 'ETH'
            token_one_address = ETH_ADDRESS
            token_one_decimals = 18
            token_two_name = 'USDC'
            token_two_address = USDC_ADDRESS
            token_two_decimals = 6
        elif (token_one_address == USDT_ADDRESS and token_two_address == USDC_ADDRESS) or (token_one_address == USDC_ADDRESS and token_two_address == USDT_ADDRESS):
            if dex_name == 'jediswap':
                pooled_token_data = DefaultContractData.get_data_from_contract(
                    0x05801bdad32f343035fb242e98d1e9371ae85bc1543962fedea16c59b35bd19b)
            token_one_name = 'USDC'
            token_one_address = USDC_ADDRESS
            token_one_decimals = 6
            token_two_name = 'USDT'
            token_two_address = USDT_ADDRESS
            token_two_decimals = 6

        pooled_token_address = pooled_token_data.get('address')
        pooled_token_name = pooled_token_data.get('name')
        balanceOf_first = await client.get_balance(token_address=token_one_address, decimals=token_one_decimals)
        balanceOf_second = await client.get_balance(token_address=token_two_address, decimals=token_two_decimals)

        if balanceOf_second.Wei <= 0 or balanceOf_first.Wei <= 0:
            return {}

        if token_one_name == 'ETH':
            eth_price = client.get_eth_price(token='ETH')
            eth_in_usd = float(balanceOf_first.Ether) * eth_price
            usd_in_crypto = float(balanceOf_second.Ether)
            min_balance = (min(eth_in_usd, usd_in_crypto)) * 90/100
            amount_in_usdt = uniform(0.1, float(min_balance))
            amount_one = TokenAmount(amount=(float(amount_in_usdt) / eth_price))
            amount_two = TokenAmount(amount=eth_price * float(amount_one.Ether), decimals=6)
        elif (token_one_name == 'USDT' and token_two_name == 'USDC') or (
                token_one_name == 'USDC' and token_two_name == 'USDT'):
            amount_in_usdt = uniform(0.1, float(min([balanceOf_first.Ether, balanceOf_second.Ether])))
            token_one_address = USDT_ADDRESS
            token_two_address = USDC_ADDRESS
            amount_one = amount_in_usdt
            amount_two = amount_in_usdt

        if amount_one and amount_two and amount_in_usdt:
            return {'pooled_token_address': pooled_token_address,
                    'pooled_token_name': pooled_token_name,
                    'amount_one': amount_one,
                    'amount_two': amount_two,
                    'amount_in_usdt': amount_in_usdt,
                    'token_one_address': token_one_address,
                    'token_two_address': token_two_address,
                    'token_one_name': token_one_name,
                    'token_two_name': token_two_name,
                    'token_one_decimals': token_one_decimals,
                    'token_two_decimals': token_two_decimals}
    except Exception as exc:
        logger.error(f"[{client.address}] Couldn't get data for adding liquidity | {exc}")


async def get_data_for_swap(client: Client, swap_to_eth):
    for _ in range(15):
        data =  await _get_data_for_swap(client=client, swap_to_eth=swap_to_eth)
        if data != {}:
            return data


async def get_data_for_liquidity_pool(client: Client, dex_name: str):
    for _ in range(15):
        data =  await _get_data_for_liquidity_pool(client=client, dex_name=dex_name)
        if data != {}:
            return data
