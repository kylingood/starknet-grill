MAX_GWEI = 20

# Increase random max gas usage for every transaction in percents
RANDOM_INCREASE_FEE = [15, 30]

# Max slippage for swaps in percents
SLIPPAGE = 2

""" Your free node url from Infura"""
NODE_URL = ''

# Use proxy for web3
USE_PROXY = False

# Delay in seconds between every task
DELAY_BETWEEN_ACTIONS = [0, 120]

# Initial delay between accounts
INITIAL_DELAY = [0, 50]

# Minimal amount for swap in percentage. E.g., if you have 100$ on balance, the amount of each swap will be 10-20$
PERCENTAGE_BALANCE_FOR_SWAP = [10, 20]

"-----------------------------------------------------------------------------------"

# OKX MODULE. Before enabling, you need to add your wallets to whitelist addresses in OKX
ENABLE_WITHDRAW_FROM_OKX = True
DELAY_BEFORE_WITHDRAW = [0, 120]
DELAY_AFTER_WITHDRAW = [400, 600]
ETH_TO_WITHDRAW = [0.05, 0.08]
OKX_API_KEY = 'imnot_sybil'
OKX_SECRET_KEY = 'giveme_drop_please'
OKX_PASSWORD_FROM_KEY = 'lifechange'

# OPTIONAL PARAM PROXY. \\\ {'http': 'http://log:pass@ip:port'} or False
PROXY_FOR_OKX = False

"------------------------------------------------------------------------------------"

"""Below is the modules for DEX.
True is enable module
False is disable module
 _SWAP_TX_COUNT is the transactions quantity for swap
 _POOL_TX_COUNT is the transactions quantity for deposit and withdraw to/from liquidity pools
 """

# JediSWAP MODULE
ENABLE_JEDISWAP = True
JEDISWAP_SWAP_TX_COUNT = [1, 1]
JEDISWAP_POOL_TX_COUNT = [1, 1]

# AVNUSWAP MODULE
ENABLE_AVNUSWAP = True
AVNUSWAP_SWAP_TX_COUNT = [1, 1]

# StarknetID mint (about 0.3$ cost)
ENABLE_STARKNETID_MINT = True
STARKNETID_TX_COUNT = [1, 1]

# DMAIL MODULE
ENABLIE_DMAIL = True
DMAIL_TX_COUNT = [1, 1]
