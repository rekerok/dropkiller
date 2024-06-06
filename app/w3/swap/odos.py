import requests
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from app.config import APIS
from . import Swapper
from app.models import contracts


class Odos(Swapper):
    name = "odos"
    url = "https://app.odos.xyz/"
    support_networks = [
        "arbitrum_one",
        "base",
        "ethereum",
        "optimism",
        "avalanche",
        "polygon",
        "bsc",
        "zksync",
    ]
    type = "swap"

    def __init__(self, web3_client: Web3Client, slippage: float = 5) -> None:
        super().__init__(web3_client=web3_client, slippage=slippage)
        self.contract = self.web3_client.get_contract(
            address=contracts["odos"]["contracts"][self.web3_client.network["name"]],
            abi=contracts["odos"]["abi"],
        )

    def _get_quote(
        self,
        from_token: Token_Info = None,
        to_token: Token_Info = None,
        amount: Token_Amount = None,
    ):
        data = {
            "chainId": self.web3_client.w3.eth.chain_id,
            "inputTokens": [
                {"tokenAddress": from_token.address, "amount": str(amount.wei)}
            ],
            "outputTokens": [{"tokenAddress": to_token.address, "proportion": 1}],
            "userAddr": self.web3_client.address,
            "slippageLimitPercent": self.slippage,
            "compact": False,
            "referralCode": 2334531771,
        }

        response = requests.post(
            APIS.ODOS + "quote/v2",
            headers={"Content-Type": "application/json"},
            json=data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def _get_assemble(self, path_id):
        data = {
            "userAddr": self.web3_client.address,
            "pathId": path_id,
            "simulate": False,
        }

        response = requests.post(
            APIS.ODOS + "assemble",
            headers={"Content-Type": "application/json"},
            json=data,
        )

        if response.status_code == 200:
            assembled_transaction = response.json()
            return assembled_transaction
        else:
            return None

    def _execute_swap(
        self, amount: Token_Amount, from_token: Token_Info, to_token: Token_Info
    ):
        if Token_Info.is_native_token(
            network=self.web3_client.network, token=from_token
        ):
            from_token.address = "0x0000000000000000000000000000000000000000"
        if Token_Info.is_native_token(network=self.web3_client.network, token=to_token):
            to_token.address = "0x0000000000000000000000000000000000000000"
        quote = self._get_quote(from_token=from_token, to_token=to_token, amount=amount)
        assemble = self._get_assemble(path_id=quote["pathId"])
        return self.web3_client.send_transaction(
            from_token=from_token,
            to_address=self.contract.address,
            amount=amount,
            data=assemble["transaction"]["data"],
        )
