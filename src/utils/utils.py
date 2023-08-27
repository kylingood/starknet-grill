import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(os.path.join(ROOT_DIR), 'abis')
ACCOUNTS_DIR = os.path.join(os.path.join(ROOT_DIR), 'accounts')
ACC_DIR = os.path.join(os.path.join(ACCOUNTS_DIR,), 'accounts.txt')
PROXY_DIR = os.path.join(os.path.join(ACCOUNTS_DIR), 'proxy.txt')

JEDISWAP_ABI_PATH = os.path.join(ABIS_DIR, 'jediswap.json')
AVNUSWAP_ABI_PATH = os.path.join(ABIS_DIR, 'avnuswap.json')
STARKNETID_ABI_PATH = os.path.join(ABIS_DIR, 'starknetid.json')

ETH_ABI_PATH = os.path.join(ABIS_DIR, 'eth.json')
USDT_ABI_PATH = os.path.join(ABIS_DIR, 'usdt.json')
USDC_ABI_PATH = os.path.join(ABIS_DIR, 'usdc.json')
DAI_ABI_PATH = os.path.join(ABIS_DIR, 'dai.json')

JEDISWAP_ETHUSDC_ABI_PATH = os.path.join(ABIS_DIR, 'jediswap_ethusdc.json')
JEDISWAP_ETHUSDT_ABI_PATH = os.path.join(ABIS_DIR, 'jediswap_ethusdt.json')
JEDISWAP_USDCUSDT_ABI_PATH = os.path.join(ABIS_DIR, 'jediswap_usdcusdt.json')

DMAIL_ABI_PATH = os.path.join(ABIS_DIR, 'dmail.json')

with open(ACC_DIR, 'r') as file:
    ACCOUNTS_LIST = [x.rstrip() for x in file.readlines()]

with open(PROXY_DIR, 'r') as file:
    PROXY_ADDRESSES_LIST = [x.rstrip() for x in file.readlines()]
    PROXY_ITER = iter(PROXY_ADDRESSES_LIST)
