from decimal import Decimal
from pathlib import Path
from typing import List

import web3
from eth_account.signers.local import LocalAccount
from eth_typing import URI, ChecksumAddress

from velero_bot_sdk.contracts.base import BaseContractConnector
from velero_bot_sdk.contracts.utils import calc_perc


class WagyuContractConnector(BaseContractConnector):
    _router_addr: ChecksumAddress
    _multicall_addr: ChecksumAddress

    def __init__(self, http_rpc_url: URI, abi_dir: Path, router_addr: str, multicall_addr: str,
                 slippage: Decimal = Decimal("0.5"), external_block_explorer_url: str = None,
                 rpc_timeout: int = 60, account: LocalAccount = None):
        super().__init__(http_rpc_url=http_rpc_url, abi_dir=abi_dir, account=account,
                         external_block_explorer_url=external_block_explorer_url, rpc_timeout=rpc_timeout)

        self._router_addr = web3.Web3.toChecksumAddress(router_addr)
        self._factory_addr = self.router.caller.factory()
        self.slippage = slippage

        self._multicall_addr = web3.Web3.toChecksumAddress(multicall_addr)
        self._wrapped_coin_addr = self.router.caller.WETH()

    @property
    def router(self):
        return self.get_contract(contract=self._router_addr, abi_file_name="PancakeRouter.abi")

    @property
    def factory(self):
        return self.get_contract(contract=self._factory_addr, abi_file_name="PancakeFactory.abi")

    @property
    def multicall(self):
        return self.get_contract(contract=self._multicall_addr, abi_file_name="Multicall2.abi")

    def get_amount_out(self, amount_in: Decimal, path: List[str]):
        return self.router.caller.getAmountsOut(amountIn=int(amount_in), path=path)[-1]

    def get_amount_in(self, amount_out: Decimal, path: List[str]):
        return self.router.caller.getAmountsIn(amountOut=int(amount_out), path=path)[0]

    def swap_exact_coins_for_tokens(self, amount_in: Decimal, path: List[str],
                                    min_amount_out: Decimal = None, slippage: Decimal = None):
        assert amount_in > 0, "amount to be exchanged must be greater than 0"
        assert len(path) >= 1, "path length must be greater than 1 token"

        if min_amount_out is not None:
            min_amount_out = int(min_amount_out)
        else:
            slippage = slippage or Decimal("-1") * self.slippage
            min_amount_out = int(calc_perc(Decimal(self.get_amount_out(amount_in, path)), slippage))

        assert min_amount_out > 0, "min_amount_out must be greater than 0"

        raw_tx = self.router.functions.swapExactETHForTokens(
            amountOutMin=min_amount_out,
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        self.logger.info(f"swap exact {amount_in} coins for approximately {min_amount_out} tokens for path {path}")
        return self.call_tx(raw_tx, int(amount_in))

    def swap_exact_tokens_for_coins(self, amount_in: Decimal, path: List[str],
                                    min_amount_out: Decimal = None, slippage: Decimal = None):
        assert amount_in > 0, "amount to be exchanged must be greater than 0"
        assert len(path) >= 2, "path length must be greater than 1 token"

        if min_amount_out is not None:
            min_amount_out = int(min_amount_out)
        else:
            slippage = slippage or Decimal("-1") * self.slippage
            min_amount_out = int(calc_perc(Decimal(self.get_amount_out(amount_in, path)), slippage))

        self.logger.info(f"swap exact {amount_in} tokens for approximately {min_amount_out} coins for path {path}")
        assert min_amount_out > 0, "min_amount_out must be greater than 0"

        raw_tx = self.router.functions.swapExactTokensForETH(
            amountIn=int(amount_in),
            amountOutMin=min_amount_out,
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        return self.call_tx(raw_tx)

    def swap_exact_tokens_for_tokens(self, amount_in: Decimal, path: List[str],
                                     min_amount_out: Decimal = None, slippage: Decimal = None):
        assert amount_in > 0, "amount to be exchanged must be greater than 0"
        assert len(path) >= 2, "path length must be greater than 1 token"

        if min_amount_out is not None:
            min_amount_out = int(min_amount_out)
        else:
            slippage = slippage or Decimal("-1") * self.slippage
            min_amount_out = int(calc_perc(Decimal(self.get_amount_out(amount_in, path)), slippage))

        assert min_amount_out > 0, "min_amount_out must be greater than 0"

        raw_tx = self.router.functions.swapExactTokensForTokens(
            amountIn=int(amount_in),
            amountOutMin=min_amount_out,
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        self.logger.info(f"swap exact {amount_in} tokens for approximately {min_amount_out} tokens for path {path}")

        return self.call_tx(raw_tx)

    def swap_coin_for_exact_tokens(self, amount_out: Decimal, path: List[str],
                                   max_amount_in: Decimal = None, slippage: Decimal = None):
        assert amount_out > 0, "amount must be greater than 0"
        assert len(path) >= 1, "path length must be greater than 1 token"

        if max_amount_in is not None:
            max_amount_in = int(max_amount_in)
        else:
            max_amount_in = int(calc_perc(Decimal(self.get_amount_in(amount_out, path)), slippage or self.slippage))

        assert max_amount_in > 0, "max_amount_in must be greater than 0"

        raw_tx = self.router.functions.swapETHForExactTokens(
            amountOutMin=int(amount_out),
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        self.logger.info(f"swap approximately {max_amount_in} coins for exact {amount_out} tokens for path {path}")

        return self.call_tx(raw_tx, max_amount_in)

    def swap_tokens_for_exact_coins(self, amount_out: Decimal, path: List[str],
                                    max_amount_in: Decimal = None, slippage: Decimal = None):
        assert amount_out > 0, "amount to be exchanged must be greater than 0"
        assert len(path) >= 2, "path length must be greater than 1 token"

        if max_amount_in is not None:
            max_amount_in = int(max_amount_in)
        else:
            int(calc_perc(Decimal(self.get_amount_in(amount_out, path)), slippage or self.slippage))

        assert max_amount_in > 0, "max_amount_in must be greater than 0"

        raw_tx = self.router.functions.swapTokensForExactETH(
            amountOut=int(amount_out),
            amountInMax=max_amount_in,
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        self.logger.info(f"swap approximately {max_amount_in} token for exact {amount_out} coins for path {path}")

        return self.call_tx(raw_tx)

    def swap_tokens_for_exact_tokens(self, amount_out: Decimal, path: List[str],
                                     max_amount_in: Decimal = None, slippage: Decimal = None):
        assert amount_out > 0, "amount to be exchanged must be greater than 0"
        assert len(path) >= 2, "path length must be greater than 1 token"

        if max_amount_in is not None:
            max_amount_in = int(max_amount_in)
        else:
            int(calc_perc(Decimal(self.get_amount_in(amount_out, path)), slippage or self.slippage))

        assert max_amount_in > 0, "max_amount_in must be greater than 0"

        raw_tx = self.router.functions.swapTokensForExactTokens(
            amountOut=int(amount_out),
            amountInMax=max_amount_in,
            path=path,
            to=self.account.address,
            deadline=self.multicall.caller.getCurrentBlockTimestamp() + 30
        )

        self.logger.info(f"swap approximately {max_amount_in} tokens for exact {amount_out} tokens for path {path}")

        return self.call_tx(raw_tx)
