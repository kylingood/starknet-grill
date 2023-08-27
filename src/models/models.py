from src.utils.utils import (JEDISWAP_ABI_PATH,
                             ETH_ABI_PATH,
                             USDT_ABI_PATH,
                             USDC_ABI_PATH,
                             JEDISWAP_ETHUSDC_ABI_PATH,
                             JEDISWAP_ETHUSDT_ABI_PATH,
                             JEDISWAP_USDCUSDT_ABI_PATH,
                             DMAIL_ABI_PATH,
                             DAI_ABI_PATH,
                             AVNUSWAP_ABI_PATH,
                             STARKNETID_ABI_PATH
                             )
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

import json


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals


@dataclass
class DefaultContractData:
    ETH_CONTRACT = {'address': 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
                    'abi': json.load(open(ETH_ABI_PATH)),
                    'name': 'ETH', 'decimals': 18}
    USDT_CONTRACT = {'address': 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8,
                     'abi': json.load(open(USDT_ABI_PATH)),
                     'name': 'USDT', 'decimals': 6}
    USDC_CONTRACT = {'address': 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
                     'abi': json.load(open(USDC_ABI_PATH)),
                     'name': 'USDC', 'decimals': 6}

    JEDISWAP_CONTRACT = {'address': 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023,
                         'abi': json.load(open(JEDISWAP_ABI_PATH))}

    JEDISWAP_ETHUSDC_CONTRACT = {'address': 0x04d0390b777b424e43839cd1e744799f3de6c176c7e32c1812a41dbd9c19db6a,
                                 'abi': json.load(open(JEDISWAP_ETHUSDC_ABI_PATH)),
                                 'name': 'ETHUSDC JediSwap',
                                 'decimals': 18}

    JEDISWAP_ETHUSDT_CONTRACT = {'address': 0x045e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6,
                                 'abi': json.load(open(JEDISWAP_ETHUSDT_ABI_PATH)),
                                 'name': 'ETHUSDT Jediswap',
                                 'decimals': 18}

    JEDISWAP_USDCUSDT_CONTRACT = {'address': 0x05801bdad32f343035fb242e98d1e9371ae85bc1543962fedea16c59b35bd19b,
                                  'abi': json.load(open(JEDISWAP_USDCUSDT_ABI_PATH)),
                                  'name': 'USDCUSDT Jediswap',
                                  'decimals': 18}

    DMAIL_CONTRACT = {'address': 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309,
                      'abi': json.load(open(DMAIL_ABI_PATH))}

    DAI_CONTRACT = {'address': 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3,
                    'abi': json.load(open(DAI_ABI_PATH)),
                    'name': 'DAI', 'decimals': 18}

    AVNUSWAP_CONTRACT = {'address': 0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f,
                         'abi': json.load(open(AVNUSWAP_ABI_PATH))}


    JEDISWAP_DAIETH_CONTRACT = {'address': 0x07e2a13b40fc1119ec55e0bcf9428eedaa581ab3c924561ad4e955f95da63138}

    JEDISWAP_DAIUSDC_CONTRACT = {'address': 0x00cfd39f5244f7b617418c018204a8a9f9a7f72e71f0ef38f968eeb2a9ca302b}

    JEDISWAP_DAIUSDT_CONTRACT = {'address': 0x00f0f5b3eed258344152e1f17baf84a2e1b621cd754b625bec169e8595aea767}

    STARKNETID_CONTRACT = {'address': 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af,
                           'abi': json.load(open(STARKNETID_ABI_PATH))}

    @staticmethod
    def get_data_from_contract(contract) -> dict:
        if contract == 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7:
            return DefaultContractData.ETH_CONTRACT
        elif contract == 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8:
            return DefaultContractData.USDT_CONTRACT
        elif contract == 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8:
            return DefaultContractData.USDC_CONTRACT
        elif contract == 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3:
            return DefaultContractData.DAI_CONTRACT

        # jediswap
        elif contract == 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023:
            return DefaultContractData.JEDISWAP_CONTRACT
        elif contract == 0x04d0390b777b424e43839cd1e744799f3de6c176c7e32c1812a41dbd9c19db6a:
            return DefaultContractData.JEDISWAP_ETHUSDC_CONTRACT
        elif contract == 0x045e7131d776dddc137e30bdd490b431c7144677e97bf9369f629ed8d3fb7dd6:
            return DefaultContractData.JEDISWAP_ETHUSDT_CONTRACT
        elif contract == 0x05801bdad32f343035fb242e98d1e9371ae85bc1543962fedea16c59b35bd19b:
            return DefaultContractData.JEDISWAP_USDCUSDT_CONTRACT

        # dmail
        elif contract == 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309:
            return DefaultContractData.DMAIL_CONTRACT

        # avnu
        elif contract == 0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f:
            return DefaultContractData.AVNUSWAP_CONTRACT

        # starknetid
        elif contract == 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af:
            return DefaultContractData.STARKNETID_CONTRACT