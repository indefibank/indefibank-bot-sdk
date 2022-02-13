import json
import logging
from functools import wraps
from pathlib import Path
from typing import Dict

import web3
from eth_account.signers.local import LocalAccount
from eth_typing import URI
from hexbytes import HexBytes
from web3.contract import Contract, ContractFunction

from velero_bot_sdk.contracts.utils import BlockScout


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if len(args) > 1 and isinstance(args[0], BaseContractConnector):
                self = args[0]
                logger = self.logger
            else:
                logger = logging.getLogger(func.__name__)
            extra_info = {
                "func": func.__name__,
                "position_arguments": args,
                "keywords_arguments": kwargs
            }
            logger.error(f"{func.__name__} call failed", exc_info=True, extra=extra_info)

            raise e

    return wrapper


class BaseContractConnector:
    _abi_dir: Path
    account: LocalAccount
    logger: logging.Logger
    external_block_explorer: BlockScout

    def __init__(self, http_rpc_url: URI, abi_dir: Path,
                 external_block_explorer_url: str = None, rpc_timeout: int = 60, account: LocalAccount = None):
        self.web3 = web3.Web3(web3.HTTPProvider(http_rpc_url, request_kwargs={"timeout": rpc_timeout}))
        self._abi_dir = abi_dir
        self.account = account
        self.web3.eth.default_account = account.address
        self.logger = logging.getLogger(self.__class__.__name__)
        self.external_block_explorer = BlockScout(base_url=external_block_explorer_url) \
            if external_block_explorer_url is not None else None

    @error_handler
    def get_abi(self, file_name: str, _dir: Path = None) -> Dict:
        _dir = _dir or self._abi_dir
        with (_dir / file_name).open() as file:
            return json.load(file)

    @error_handler
    def get_contract(self, contract: str, abi_file_name: str, _abi_dir: Path = None) -> Contract:
        address = web3.Web3.toChecksumAddress(contract)

        if not (_abi_dir if _abi_dir is not None else self._abi_dir / abi_file_name).exists():
            abi = self.external_block_explorer.get_contract_abi(address)
            with (_abi_dir if _abi_dir is not None else self._abi_dir / abi_file_name).open(mode="w") as file:
                json.dump(abi, file)
        else:
            abi = self.get_abi(file_name=abi_file_name, _dir=_abi_dir)

        return self.web3.eth.contract(address=address, abi=abi)

    def call_tx(self, contract_method: ContractFunction, value: int = 0) -> HexBytes:
        nonce = self.web3.eth.getTransactionCount(self.account.address, 'pending')
        raw_tx = contract_method.buildTransaction({"nonce": nonce, "gasPrice": self.web3.eth.gas_price, "value": value})
        try:
            tx_hash = self.web3.eth.sendRawTransaction(self.account.sign_transaction(raw_tx).rawTransaction.hex())
        except Exception as e:
            self.logger.error("Failed call contract Method", exc_info=e)
            raise e

        return tx_hash
