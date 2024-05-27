import requests
from app.w3.bridge.bridger import Bridger
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from app.config import APIS


class Nitro_Bridge(Bridger):

    def __init__(
        self,
        web3_client: Web3Client,
        slippage: float = 5,
    ) -> None:
        super().__init__(web3_client=web3_client, slippage=slippage)

    @classmethod
    def get_quote(
        cls,
        amount: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
        from_chain_id: int,
        to_chain_id: str,
    ) -> dict:
        url = APIS.NITRO + "quote/"
        params = {
            "amount": str(amount.wei),
            "fromTokenAddress": str(from_token.address),
            "fromTokenChainId": str(from_chain_id),
            "toTokenAddress": str(to_token.address),
            "toTokenChainId": str(to_chain_id),
        }
        response = requests.get(url=url, params=params)
        if not response:
            return None
        return response.json()

    @classmethod
    def get_transaction(cls, quote: dict) -> dict:
        url = APIS.NITRO + "transaction/"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, json=quote)
        if not response:
            return None
        return response.json()

    def _execute_bridge(
        self,
        amount: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
        to_network: dict,
    ):
        from_chain_id: int = int(self.web3_client.w3.eth.chain_id)
        to_chain_id: int = int(to_network["chainId"])
        if from_token.address == "":
            from_token.address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        if to_token.address == "":
            to_token.address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        quote = Nitro_Bridge.get_quote(
            amount=amount,
            from_token=from_token,
            to_token=to_token,
            from_chain_id=from_chain_id,
            to_chain_id=to_chain_id,
        )
        quote.update(
            {
                "senderAddress": self.web3_client.address,
                "receiverAddress": self.web3_client.address,
            }
        )
        transaction = Nitro_Bridge.get_transaction(quote=quote)
        return self.web3_client.send_transaction(
            from_token=from_token,
            to_address=transaction["txn"]["to"],
            amount=amount,
            data=transaction["txn"]["data"],
        )
