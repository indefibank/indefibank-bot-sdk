from decimal import Decimal
from pathlib import Path
from typing import Dict

import web3
from eth_account.signers.local import LocalAccount
from eth_typing import URI, ChecksumAddress
from web3.contract import Contract

from velero_bot_sdk.contracts.base import BaseContractConnector, error_handler
from velero_bot_sdk.contracts.utils import Converter


class BaseDssContractConnector(BaseContractConnector):
    _chain_log_addr: str
    _ilk_registry_addr: str

    def __init__(self, http_rpc_url: URI, abi_dir: Path, chain_log_addr: str,
                 external_block_explorer_url: str = None, rpc_timeout: int = 60, account: LocalAccount = None):
        super().__init__(http_rpc_url=http_rpc_url, abi_dir=abi_dir, rpc_timeout=rpc_timeout,
                         external_block_explorer_url=external_block_explorer_url, account=account)
        self._chain_log_addr = chain_log_addr
        self._ilk_registry_addr = self.get_contact_address("ILK_REGISTRY")

        self.ilk_list = list(map(lambda x: Converter.bytes32_to_str(x), self.ilk_registry.caller.list()))

    def get_contract(self, contract: str, abi_file_name: str, _abi_dir: Path = None) -> Contract:
        address = contract if web3.Web3.isAddress(contract) else self.get_contact_address(contract)
        return super().get_contract(contract=address, abi_file_name=abi_file_name, _abi_dir=_abi_dir)

    @error_handler
    def get_contact_address(self, name: str) -> ChecksumAddress:
        return web3.Web3.toChecksumAddress(self.chain_log.functions.getAddress(Converter.str_to_bytes32(name)).call())

    @property
    def chain_log(self) -> Contract:
        return self.get_contract(contract=self._chain_log_addr, abi_file_name="ChainLog.abi")

    @property
    def ilk_registry(self) -> Contract:
        return self.get_contract(contract=self._ilk_registry_addr, abi_file_name="IlkRegistry.abi")


class DssContractsConnector(BaseDssContractConnector):
    _vat_addr: str
    _dog_addr: str
    _cat_addr: str
    _vow_addr: str
    _pot_addr: str
    _spot_addr: str
    _cdp_manager_addr: str
    _multicall_addr: str
    _mcd_gov_addr: str
    _mcd_iou_addr: str
    _chief_addr: str
    _jug_addr: str
    _join_main_stable_addr: str
    _flap_addr: str
    _flop_addr: str
    _flash_addr: str
    _vote_proxy_factory_addr: str
    _vote_delegate_proxy_factory_addr: str
    _get_cdps_addr: str
    _vlx_addr: str
    _usdv_addr: str

    _osm_addresses: Dict[str, str]
    _ilk_join_addresses: Dict[str, str]
    _ilk_clip_addresses: Dict[str, str]
    _ilk_clip_calc_addresses: Dict[str, str]

    def __init__(self, http_rpc_url: URI, abi_dir: Path, chain_log_addr: str,
                 external_block_explorer_url: str = None, rpc_timeout: int = 60, account: LocalAccount = None):
        super().__init__(http_rpc_url=http_rpc_url, abi_dir=abi_dir, rpc_timeout=rpc_timeout, account=account,
                         chain_log_addr=chain_log_addr, external_block_explorer_url=external_block_explorer_url)

        self.load_dss()

    def load_dss(self):
        self.ilk_list = list(map(lambda x: Converter.bytes32_to_str(x), self.ilk_registry.caller.list()))

        self._vat_addr = self.get_contact_address("MCD_VAT")
        self._dog_addr = self.get_contact_address("MCD_DOG")
        self._cat_addr = self.get_contact_address("MCD_CAT")
        self._vow_addr = self.get_contact_address("MCD_VOW")
        self._pot_addr = self.get_contact_address("MCD_POT")
        self._spot_addr = self.get_contact_address("MCD_SPOT")
        self._multicall_addr = self.get_contact_address("MULTICALL")
        self._cdp_manager_addr = self.get_contact_address("CDP_MANAGER")
        self._mcd_gov_addr = self.get_contact_address("MCD_GOV")
        self._mcd_iou_addr = self.get_contact_address("MCD_IOU")
        self._chief_addr = self.get_contact_address("MCD_ADM")
        self._jug_addr = self.get_contact_address("MCD_JUG")
        self._join_main_stable_addr = self.get_contact_address("MCD_JOIN_USDV")
        self._flap_addr = self.get_contact_address("MCD_FLAP")
        self._flap_addr = self.get_contact_address("MCD_FLOP")
        self._flash_addr = self.get_contact_address("MCD_FLASH")
        self._vlx_addr = self.get_contact_address("VLX")
        self._usdv_addr = self.get_contact_address("MCD_USDV")
        self._vote_proxy_factory_addr = self.get_contact_address("VOTE_PROXY_FACTORY")
        self._vote_delegate_proxy_factory_addr = self.get_contact_address("VOTE_DELEGATE_PROXY_FACTORY")
        self._get_cdps_addr = self.get_contact_address("GET_CDPS")

        self._osm_addresses = dict(
            tuple(map(lambda x: (x, self.ilk_registry.caller.pip(Converter.str_to_bytes32(x))), self.ilk_list))
        )

        self._ilk_join_addresses = dict(
            tuple(map(lambda x: (x, self.get_contact_address(f"MCD_JOIN_{x.replace('-', '_')}")), self.ilk_list))
        )

        self._ilk_clip_addresses = dict(
            tuple(map(lambda x: (x, self.get_contact_address(f"MCD_CLIP_{x.replace('-', '_')}")), self.ilk_list))
        )

        self._ilk_clip_calc_addresses = dict(
            tuple(map(lambda x: (x, self.get_contact_address(f"MCD_CLIP_CALC_{x.replace('-', '_')}")), self.ilk_list))
        )

    @error_handler
    def get_current_price(self, ilk: str) -> Decimal:
        spot = self.vat.caller.ilks(Converter.str_to_bytes32(ilk))[2]
        mat = self.spot.caller.ilks(Converter.str_to_bytes32(ilk))[1]
        return Decimal(spot * mat) / Decimal(10 ** 54)

    @property
    def vat(self) -> Contract:
        return self.get_contract(contract=self._vat_addr, abi_file_name="Vat.abi")

    @property
    def dog(self) -> Contract:
        return self.get_contract(contract=self._dog_addr, abi_file_name="Dog.abi")

    @property
    def cat(self) -> Contract:
        return self.get_contract(contract=self._cat_addr, abi_file_name="Cat.abi")

    @property
    def vow(self) -> Contract:
        return self.get_contract(contract=self._vow_addr, abi_file_name="Vow.abi")

    @property
    def pot(self) -> Contract:
        return self.get_contract(contract=self._pot_addr, abi_file_name="Pot.abi")

    @property
    def spot(self) -> Contract:
        return self.get_contract(contract=self._spot_addr, abi_file_name="Spot.abi")

    @property
    def cdp_manager(self) -> Contract:
        return self.get_contract(contract=self._cdp_manager_addr, abi_file_name="DssCdpManager.abi")

    @property
    def chief(self) -> Contract:
        return self.get_contract(contract=self._chief_addr, abi_file_name="DSChief.abi")

    @property
    def jug(self) -> Contract:
        return self.get_contract(contract=self._jug_addr, abi_file_name="Jug.abi")

    @property
    def join_main_stablecoin(self) -> Contract:
        return self.get_contract(contract=self._join_main_stable_addr, abi_file_name="UsdvJoin.abi")

    @property
    def gov_token(self) -> Contract:
        return self.get_contract(contract=self._mcd_gov_addr, abi_file_name="DSToken.abi")

    @property
    def iou_token(self) -> Contract:
        return self.get_contract(contract=self._mcd_iou_addr, abi_file_name="DSToken.abi")

    @property
    def multicall(self) -> Contract:
        return self.get_contract(contract=self._multicall_addr, abi_file_name="Multicall.abi")

    @property
    def flap(self) -> Contract:
        return self.get_contract(contract=self._flap_addr, abi_file_name="Flap.abi")

    @property
    def flop(self) -> Contract:
        return self.get_contract(contract=self._flop_addr, abi_file_name="Flop.abi")

    @property
    def flash(self) -> Contract:
        return self.get_contract(contract=self._flash_addr, abi_file_name="Flash.abi")

    @property
    def vlx(self) -> Contract:
        return self.get_contract(contract=self._vlx_addr, abi_file_name="VLX.abi")

    @property
    def usdv(self) -> Contract:
        return self.get_contract(contract=self._usdv_addr, abi_file_name="USDV.abi")

    @property
    def getcdps(self) -> Contract:
        return self.get_contract(contract=self._get_cdps_addr, abi_file_name="GetCDPS.abi")

    @property
    def vote_proxy_factory(self) -> Contract:
        return self.get_contract(contract=self._vote_proxy_factory_addr, abi_file_name="VoteProxyFactory.abi")

    @property
    def vote_delegate_proxy_factory(self) -> Contract:
        return self.get_contract(contract=self._vote_delegate_proxy_factory_addr,
                                 abi_file_name="VoteDelegateProxyFactory.abi")

    def get_ilk_osm(self, ilk: str) -> Contract:
        return self.get_contract(contract=self._osm_addresses[ilk], abi_file_name="OSM.abi")

    def get_ilk_join(self, ilk: str) -> Contract:
        return self.get_contract(contract=self._ilk_join_addresses[ilk], abi_file_name="GemJoin.abi")

    def get_ilk_clip(self, ilk: str) -> Contract:
        return self.get_contract(contract=self._ilk_clip_addresses[ilk], abi_file_name="Clipper.abi")

    def get_ilk_clip_calc(self, ilk: str) -> Contract:
        return self.get_contract(contract=self._ilk_clip_calc_addresses[ilk], abi_file_name="ClipCalc.abi")

    def get_ds_proxy(self, address: str) -> Contract:
        return self.get_contract(contract=address, abi_file_name="DSProxy.abi")
