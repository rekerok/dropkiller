import eth_utils
import requests
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from . import Swapper
from app.config import APIS, ONE_INCH_KEY


class One_Inch(Swapper):

    def __init__(self, web3_client: Web3Client, slippage: float = 5) -> None:
        super().__init__(web3_client=web3_client, slippage=slippage)

    def _get_spender(
        self,
    ):
        url = APIS.ONE_INCH + str(self.web3_client.w3.eth.chain_id) + "/approve/spender"
        headers = {
            "Authorization": f"Bearer {ONE_INCH_KEY}",
            "accept": "application/json",
        }
        response = requests.get(url=url, headers=headers)
        if not response:
            return None
        return response

    def _get_swap_data(
        self, from_token: Token_Info, to_token: Token_Info, amount: Token_Amount
    ):
        url = APIS.ONE_INCH + str(self.web3_client.w3.eth.chain_id) + "/swap"
        headers = {
            "Authorization": f"Bearer {ONE_INCH_KEY}",
            "accept": "application/json",
        }
        params = {
            "src": from_token.address,
            "dst": to_token.address,
            "amount": amount.wei,
            "from": self.web3_client.address,
            "slippage": self.slippage,
        }

        response = requests.get(url=url, headers=headers, params=params)
        if not response:
            return None
        return response

    def _get_swap_data(
        self, from_token: Token_Info, to_token: Token_Info, amount: Token_Amount
    ):
        url = APIS.ONE_INCH + str(self.web3_client.w3.eth.chain_id) + "/swap"
        headers = {
            "Authorization": f"Bearer {ONE_INCH_KEY}",
            "accept": "application/json",
        }
        params = {
            "chain": str(self.web3_client.w3.eth.chain_id),
            "src": from_token.address,
            "dst": to_token.address,
            "amount": amount.wei,
            "from": self.web3_client.address,
            "slippage": self.slippage,
        }

        response = requests.get(url=url, headers=headers, params=params)
        if not response:
            return None
        return response

    def _get_approve_data(self, from_token: Token_Info, amount: Token_Amount):
        url = (
            APIS.ONE_INCH
            + str(self.web3_client.w3.eth.chain_id)
            + "/approve/transaction"
        )
        headers = {
            "Authorization": f"Bearer {ONE_INCH_KEY}",
            "accept": "application/json",
        }
        params = {
            "chain": from_token.address,
            "tokenAddress": from_token.address,
            "amount": amount.wei,
        }

        response = requests.get(url=url, headers=headers, params=params)
        if not response:
            return None
        return response

    def _execute_swap(
        self, amount: Token_Amount, from_token: Token_Info, to_token: Token_Info
    ):
        if Token_Info.is_native_token(
            network=self.web3_client.network, token=from_token
        ):
            from_token.address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        if Token_Info.is_native_token(network=self.web3_client.network, token=to_token):
            to_token.address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        spender = self._get_spender()
        if spender:
            spender = eth_utils.address.to_checksum_address(
                spender.json().get("address")
            )
        else:
            return None

        if (
            from_token.address.lower()
            != "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE".lower()
            and self.web3_client.check_approve(
                token=from_token, spender=spender, amount=amount
            )
        ):
            return self.web3_client.send_transaction(
                from_token=from_token,
                to_address=from_token.address,
                amount=amount,
            )

        data = self._get_swap_data(
            from_token=from_token, to_token=to_token, amount=amount
        )
        return self.web3_client.send_transaction(
            from_token=from_token,
            to_address=spender,
            amount=amount,
            data=data.json().get("data"),
        )
