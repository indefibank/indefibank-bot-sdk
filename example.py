from pathlib import Path

import web3
from eth_account.signers.base import BaseAccount
from eth_typing import URI

from indefibank_bot_sdk.contracts.dss import DssContractsConnector

HTTP_RPC_URL = URI('https://rpc-mumbai.maticvigil.com/')
_w3 = web3.Web3(web3.HTTPProvider(HTTP_RPC_URL))

CHANGELOG = "0x4dA91D64aB3f5eb129163032F3317704bfFFfF2f"
PK = "b43b11ebe0523b0c7dc1ef3ef37cc1ce1924fbdbd3bbfcd615dbef5d52ab6fb7"  # test permit
BASE_DIR = Path(__file__).resolve().parent
ABI_PATH = BASE_DIR / 'indefibank_bot_sdk' / 'contracts' / 'abi'
ACCOUNT: BaseAccount = web3.Web3().eth.account.from_key(PK)

dss = DssContractsConnector(http_rpc_url=HTTP_RPC_URL, abi_dir=ABI_PATH, chain_log_addr=CHANGELOG, account=ACCOUNT)
