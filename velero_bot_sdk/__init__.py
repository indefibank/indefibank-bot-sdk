"""
Velero Bot SDK
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2022 by velerofinance
"""
from pathlib import Path

from velero_bot_sdk.contracts.dss import DssContractsConnector
from velero_bot_sdk.contracts.wagyu import WagyuContractConnector
from velero_bot_sdk.contracts.utils import calc_perc, Converter
from velero_bot_sdk.calulations.formuls import VeleroFormuls


VELERO_DEFAULT_ABI_DIR = Path(__file__).parent / "contracts" / "abi"


__all__ = [
    'DssContractsConnector',
    'WagyuContractConnector',
    'calc_perc',
    'Converter',
    'VELERO_DEFAULT_ABI_DIR',
]
