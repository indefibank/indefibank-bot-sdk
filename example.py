from pathlib import Path

import web3
from eth_account.signers.base import BaseAccount
from eth_typing import URI

from indefibank_bot_sdk.contracts.dss import DssContractsConnector

HTTP_RPC_URL = URI('https://mainnet.velas.com/rpc')
_w3 = web3.Web3(web3.HTTPProvider(HTTP_RPC_URL))

CHANGELOG = "0x87986E3AC1F67aDc36027Df78fBfc06CbB36E768"
# PK = "0x76ae2af4794ffe1c928fa5f4f2c145eb7343307997b448e3042056eaeff6675b"  # dev
PK = "b43b11ebe0523b0c7dc1ef3ef37cc1ce1924fbdbd3bbfcd615dbef5d52ab6fb7"  # test permit
BASE_DIR = Path(__file__).resolve().parent
ABI_PATH = BASE_DIR / 'indefibank_bot_sdk' / 'contracts' / 'abi'
ACCOUNT: BaseAccount = web3.Web3().eth.account.from_key(PK)

dss = DssContractsConnector(http_rpc_url=HTTP_RPC_URL, abi_dir=ABI_PATH, chain_log_addr=CHANGELOG, account=ACCOUNT)


if __name__ == '__main__':
    c = dss.web3.eth.get_code("0xCC9D0895AE3e8Ce578346C92cd0563ae3526A55b")
    receipt_tx = dss.web3.eth.wait_for_transaction_receipt(transaction_hash="0x319c6ae4b120e533bfb2b2dd48d7777185f38fb98e903297aed28cd47d18ed2a", timeout=30)
    # dss.get_ilk_median("BUSD-A").events.Poke().processReceipt(receipt_tx)
    print(c)
