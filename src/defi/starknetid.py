import random

from src.client.client import Client
from src.models.models import DefaultContractData
from src.logger import logger
from starknet_py.contract import Contract


class StarknetID:

    StARKNETID_CONTRACT = DefaultContractData.STARKNETID_CONTRACT.get('address')
    STARKNETID_ABI = DefaultContractData.STARKNETID_CONTRACT.get('abi')

    def __init__(self, client: Client):
        self.client = client
        self.contract = Contract(address=StarknetID.StARKNETID_CONTRACT, abi=StarknetID.STARKNETID_ABI, provider=self.client.account)

    async def mint(self):
        try:
            logger.debug(
                f"[{self.client.address}] Minting domain...[StarknetID]")
            tx_hash = await self.client.send_transaction(interacted_contract=self.contract,
                                                         function_name='mint',
                                                         starknet_id=random.randint(400000, 20000000))
            if tx_hash:
                logger.success(
                    f"[{self.client.address}] Successfully minted nft | [StarknetID]")
                return True
        except Exception as exc:
            logger.error(f"[{self.client.address}] Couldn't mint domain | [StarknetID] | {exc}")
