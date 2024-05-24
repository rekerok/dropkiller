import time
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from app.config import APIS
from . import Swapper
from app.models import contracts


class Baseswap(Swapper):

    def __init__(
        self, web3_client: Web3Client, slippage: float = 5, contract=None
    ) -> None:
        super().__init__(web3_client=web3_client, slippage=slippage)
        if contract is None:
            self.contract = self.web3_client.get_contract(
                address=contracts["baseswap"],
                abi=contracts["default_swap_abi"],
            )
        else:
            self.contract = contract

    def _get_amount_out(
        self,
        amountIn: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ) -> Token_Amount:
        try:
            amounts_out = self.contract.functions.getAmountsOut(
                amountIn.wei,
                [
                    from_token.address,
                    to_token.address,
                ],
            ).call()
            amounts_out = amounts_out[1] - amounts_out[1] * self.slippage / 100
            return Token_Amount(
                amount=amounts_out, decimals=to_token.decimals, wei=True
            )
        except Exception as error:
            return None

    def _execute_swap(
        self, amount: Token_Amount, from_token: Token_Info, to_token: Token_Info
    ):
        if Token_Info.is_native_token(
            network=self.web3_client.network, token=from_token
        ):
            from_token.address = contracts["weth"][self.web3_client.network["name"]]
        if Token_Info.is_native_token(network=self.web3_client.network, token=to_token):
            to_token.address = contracts["weth"][self.web3_client.network["name"]]

        amount_in = self._get_amount_out(
            amountIn=amount,
            from_token=from_token,
            to_token=to_token,
        )
        if amount_in is None:
            return None

        path = [from_token.address, to_token.address]
        to = self.web3_client.address
        deadline = int(time.time()) + 10000

        if Token_Info.is_native_token(
            network=self.web3_client.network, token=from_token
        ):
            data = Web3Client.get_data_from_contrat(
                contract=self.contract,
                function_of_contract="swapExactETHForTokens",
                args=(amount_in.wei, path, to, deadline),
            )
        elif Token_Info.is_native_token(
            network=self.web3_client.network, token=to_token
        ):
            data = Web3Client.get_data_from_contrat(
                contract=self.contract,
                function_of_contract="swapExactTokensForETH",
                args=(amount.wei, amount_in.wei, path, to, deadline),
            )
        else:
            data = Web3Client.get_data_from_contrat(
                contract=self.contract,
                function_of_contract="swapExactTokensForTokens",
                args=(amount.wei, amount_in.wei, path, to, deadline),
            )
        return self.web3_client.send_transaction(
            from_token=from_token,
            to_address=self.contract.address,
            amount=amount,
            data=data,
        )
