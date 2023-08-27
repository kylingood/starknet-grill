# StarkNet-grill v.0.1.0

## 📜Description

❗ <span style="color:red">**WARNING: At the moment only Argent wallets are supported. Braavos wallets have not tested. Use it at your own risk!**</span>

❗ <span style="color:green">***This is a stripped-down version with a limited number of modules. If you're looking for more modules and functions, write me in***</span> <a href='https://t.me/flextive'> telegram </a>


***Available modules:***

✅***OKX*** **withdrawing**

✅***JediSwap*** **swaps/deposit/withdraw**

✅***Avnu*** **swaps**

✅**Dmail message**

✅***Mint*** **free Starknet NFT**


## 💰Donate

```
0x63f9716a17c751d97306289b22556b879ed8fb74 (any evm)
```

## ⚙️Installation


First of all, you need to install **official** ***starknet-py*** library. Here is the instruction: 
https://starknetpy.readthedocs.io/en/latest/installation.html

This is simply guide how to install it on Windows, Mac or Linux. If you're Windows user, don't forget to install **MinGW** (it is requirement in starknet-py instruction)

After successful starknet-py installation, go to project folder via 

```
cd "Your/Project/Directory"
```
Write this command
```
pip install -r requirements.txt
```


## 📄Accounts setup

Open ```./src/accounts/accounts.txt``` file

Enter your accounts' address and private_key.

Supported **accounts** format:
```
address1:privatekey1
address2:privatekey2
```


## 📄Proxy setup

If you're considering using a proxy, go to ```./src/accounts/proxy.txt``` file

Enter your proxy for every account in this format:
```
http://log:pass@ip:port
```

## 📄Config setup

Open ```./src/config.py```

Setup config to your preferences. There is a description for every setting in file. 

Register on https://www.infura.io/ and get your StarkNet node URL. This is free node with 100.000 requests/day. 
Paste it in ```NODE_URL```

## Run script

To run script, write 
```python main.py```


## Developer

- [Github](https://github.com/flexter1)
- [Telegram](https://t.me/flextive)
- [Telegram channel](https://t.me/flexterwork)
