import eth_utils
from app.abis import abis
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class BlockchainInteraction:
    def __init__(self, web3_client: Web3Client):
        self.web3_client = web3_client

    def send_transaction(
        self,
        from_token: Token_Info,
        to_address: str,
        amount: Token_Amount = None,
        data: str = None,
        value=None,
    ): ...

    def _get_allowance(self, contract, owner: str, spender: str) -> Token_Amount:
        try:
            amount_allowance = contract.functions.allowance(
                eth_utils.address.to_checksum_address(owner),
                eth_utils.address.to_checksum_address(spender),
            ).call()
            amount_allowance = Token_Amount(
                amount=amount_allowance,
                decimals=contract.functions.decimals().call(),
                wei=True,
            )
            return amount_allowance
        except Exception as error:
            return Token_Amount(amount=0)

    def get_data_for_approve(
        self, token: Token_Info, spender: str, amount: Token_Amount
    ):
        contract = self.web3_client.get_contract(
            address=eth_utils.address.to_checksum_address(token.address),
            abi=abis["erc20"],
        )

        value_approove = Token_Amount(
            amount=amount.WEI + 1,
            decimals=amount.DECIMAL,
            wei=True,
        )
        data = contract.encodeABI(
            "approve",
            args=(
                eth_utils.address.to_checksum_address(spender),
                int(value_approove.WEI),
            ),
        )
        tx_params = self.web3_client.get_data_transaction(
            to_address=token.address,
            data=data,
        )
        return tx_params

    def check_approve(self, token: Token_Info, spender: str, amount: Token_Amount):
        contract = self.web3_client.get_contract(
            address=eth_utils.address.to_checksum_address(token.address),
            abi=abis["erc20"],
        )
        allowanced: Token_Amount = self._get_allowance(
            contract=contract, owner=self.web3_client.address, spender=spender
        )
        if allowanced.WEI > amount.WEI:
            return False
        else:
            return True

    def send_transaction(
        self,
        from_token: Token_Info,
        to_address: str,
        amount: Token_Amount = None,
        data: str = None,
        value=None,
    ):
        if not Token_Info.is_native_token(
            network=self.web3_client.network, token=from_token
        ):
            need_approve = self.check_approve(
                token=from_token, spender=to_address, amount=amount
            )
            if need_approve:
                tx_approve = self.get_data_for_approve(
                    token=from_token, spender=to_address, amount=amount
                )
            type = "approve"
            params = tx_approve
        else:
            type = "transaction"
            value = amount
            params = self.web3_client.get_data_transaction(
                to_address=to_address, data=data, value=value
            )
        return {
            "type": type,
            "data": params,
            "contract": to_address,
            "address": self.web3_client.address,
            "amount": amount,
        }
