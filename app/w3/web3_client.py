import eth_utils
from web3 import Web3

from .token_amount import Token_Amount
from .token_info import Token_Info
from app.models import contracts


class Web3Client:
    def __init__(self, network: dict, timeout: int = 60, address: str = None) -> None:
        self.address = (
            "" if address is None else eth_utils.address.to_checksum_address(address)
        )
        self.network = network
        self.w3 = Web3(
            Web3.HTTPProvider(
                endpoint_uri=self.network["rpc"],
            ),
        )

    def get_gas(
        self,
    ) -> dict:
        gas_now = Token_Amount(amount=self.w3.eth.gas_price, wei=True)
        return round(gas_now.ether * 10**9, 3)

    def get_contract(self, address: str, abi: str):
        return self.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(address), abi=abi
        )

    def get_balance(self, token_address: str = None) -> Token_Amount:
        try:
            if not token_address or token_address == "":
                value = self.w3.eth.get_balance(
                    eth_utils.address.to_checksum_address(self.address)
                )
                return Token_Amount(amount=value, wei=True)
            else:
                contract_token = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(token_address),
                    abi=contracts["erc20_abi"],
                )
                value = contract_token.functions.balanceOf(self.address).call()
                return Token_Amount(
                    amount=value,
                    decimals=contract_token.functions.decimals().call(),
                    wei=True,
                )
        except Exception as error:
            # logger.error(error)
            return None

    def _get_eip1559_tx(self, tx_params: dict, increase_gas: float = 1.1):
        last_block = self.w3.eth.get_block("latest")
        base_fee = int(last_block["baseFeePerGas"] * increase_gas)
        max_priority_fee_per_gas = self.w3.eth.max_priority_fee
        tx_params["maxFeePerGas"] = int(base_fee + max_priority_fee_per_gas)
        tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        return tx_params

    def get_transaction(
        self,
        to_address: str = None,
        data: str = None,
        value: Token_Amount = None,
    ):
        try:
            tx_params = {
                "from": self.address,
                "chainId": self.w3.eth.chain_id,
                "nonce": self.w3.eth.get_transaction_count(self.address),
            }
            if to_address:
                tx_params["to"] = self.w3.to_checksum_address(to_address)

            if data:
                tx_params["data"] = data

            if value is None or value == 0:
                tx_params["value"] = 0
            else:
                tx_params["value"] = value.wei

            if self.network["eip1559"]:
                tx_params = self._get_eip1559_tx(tx_params=tx_params)
            else:
                tx_params["gasPrice"] = self.w3.eth.gas_price

            tx_params["gas"] = int(self.w3.eth.estimate_gas(tx_params) * 1.3)
            return tx_params
        except Exception as error:
            return None

    def get_data_for_approve(
        self, token: Token_Info, spender: str, amount: Token_Amount
    ):
        contract = self.get_contract(
            address=eth_utils.address.to_checksum_address(token.address),
            abi=contracts["erc20_abi"],
        )

        value_approove = Token_Amount(
            amount=amount.wei + 1,
            decimals=amount.decimals,
            wei=True,
        )

        data = Web3Client.get_data_from_contrat(
            contract=contract,
            function_of_contract="approve",
            args=(
                eth_utils.address.to_checksum_address(spender),
                int(value_approove.wei),
            ),
        )
        tx_params = self.get_transaction(
            to_address=token.address,
            data=data,
        )
        return tx_params

    @staticmethod
    def get_data_from_contrat(contract, function_of_contract: str, args: tuple = None):
        try:
            return contract.encodeABI(
                function_of_contract,
                args=args,
            )
        except Exception as error:
            return None

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

    def check_approve(self, token: Token_Info, spender: str, amount: Token_Amount):
        contract = self.get_contract(
            address=eth_utils.address.to_checksum_address(token.address),
            abi=contracts["erc20_abi"],
        )
        allowanced: Token_Amount = self._get_allowance(
            contract=contract, owner=self.address, spender=spender
        )
        if allowanced.wei > amount.wei:
            return False
        else:
            return True

    def transfer(self, to_address: str, amount, token_address: str = ""):
        token = Token_Info.get_info_token(w3_client=self, token_address=token_address)
        amount = Token_Amount(amount=amount, decimals=token.decimals)
        if Token_Info.is_native_token(network=self.network, token=token):
            return self.send_transaction(to_address=to_address, value=amount)
        else:
            contract = self.get_contract(
                address=eth_utils.address.to_checksum_address(token_address),
                abi=contracts["erc20_abi"],
            )

            data = contract.encodeABI(
                "transfer", args=(self.w3.to_checksum_address(to_address), amount.wei)
            )
            return self.send_transaction(
                from_token=token, to_address=to_address, amount=amount, data=data
            )

    def send_transaction(
        self,
        from_token: Token_Info,
        to_address: str,
        amount: Token_Amount = None,
        data: str = None,
        value=None,
    ):
        if not Token_Info.is_native_token(network=self.network, token=from_token):
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
                params = self.get_transaction(to_address=to_address, data=data)

        else:
            type = "transaction"
            value = amount
            params = self.get_transaction(to_address=to_address, data=data, value=value)
        return {
            "type": type,
            "params": params,
            "contract": to_address,
            "address": self.address,
            "amount": amount,
        }
