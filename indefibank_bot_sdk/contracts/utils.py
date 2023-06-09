from decimal import Decimal

import requests
import json

import web3


def calc_perc(value: Decimal, percent: Decimal) -> Decimal:
    return value + (value * percent / Decimal("100"))


class Converter:
    @staticmethod
    def str_to_bytes32(string):
        hex_data = web3.Web3.to_hex(text=string)
        res = hex_data.lstrip("0x")

        zero_count = 64 - len(res)

        if zero_count >= 0:
            return "0x" + res + "0" * zero_count
        else:
            raise

    @staticmethod
    def bytes32_to_str(bytes32):
        bytes32 = bytes32.hex().rstrip("0")
        if len(bytes32) % 2 != 0:
            bytes32 = bytes32 + '0'
        return bytes.fromhex(bytes32).decode('utf8')


class ExplorerError(Exception):
    def __init__(self, message: str = 'Failed to get info', details=None, exception=None):
        self.message = message
        self.details = details
        self.exception = exception

    def __str__(self):
        return f"{self.__class__.__name__} message={self.message} detail={self.details}) exception={self.exception}"


class Explorer:
    def __init__(self, base_url: str = "https://api.polygonscan.com/api", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key

    def request(self, method: str, url: str, params: dict = None, _json: dict = None):
        response = requests.request(method=method.upper(), url=url, params=params, json=_json)

        if response.ok:
            result = response.json()
            if "status" in result and result["status"] == "1":
                return json.loads(result["result"])
            raise ExplorerError(message=result.get("message", "Failed get ABI from explorer"), details=result)
        raise ExplorerError(message="Failed get ABI from explorer", details=response.raw)

    def get_contract_abi(self, address: str):
        params = {
            "module": "contract",
            "action": "getabi",
            "address": address
        }
        if self.api_key is not None:
            params["apikey"] = self.api_key
        return self.request(method="GET", url=self.base_url, params=params)
