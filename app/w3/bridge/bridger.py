from typing import Union
from app.models import get_network
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class Bridger:
    URL = None
    SUPPORT_NETWORKS = None
    TYPE = "bridge"

    def __init__(self, web3_client: Web3Client, slippage: int = 5) -> None:
        self.web3_client = web3_client
        self.slippage = slippage

    def price_impact(): ...

    def _execute_bridge(
        self,
        from_token: Token_Info,
        to_token: Token_Info,
        amount: Token_Amount,
        to_network: dict,
    ): ...

    def get_to_token_info(self, to_network: dict, to_token_address: str) -> Token_Info:
        to_token = Token_Info.get_info_token(
            w3_client=Web3Client(network=to_network), token_address=to_token_address
        )
        return to_token

    def bridge(
        self,
        amount: Union[int, float],
        to_network: dict,
        from_token_address: str = "",
        to_token_address: str = "",
    ):
        from_token = Token_Info.get_info_token(
            w3_client=self.web3_client,
            token_address=from_token_address,
        )
        to_token = self.get_to_token_info(
            to_network=to_network, to_token_address=to_token_address
        )

        amount = Token_Amount(amount=amount, decimals=from_token.decimals)
        return self._execute_bridge(
            from_token=from_token,
            to_token=to_token,
            amount=amount,
            to_network=to_network,
        )
