from app.w3.bridge.bridger import Bridger
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from app.config import APIS
from app.models import contracts


class Stargate(Bridger):
    name = "stargate"
    url = "https://stargate.finance/"
    support_networks = [
        "arbitrum_one",
        "base",
        "ethereum",
        "optimism",
        "avalanche",
        "polygon",
        "bsc",
        "scroll",
    ]
    type="bridge"

    def __init__(
        self,
        web3_client: Web3Client,
        slippage: float = 5,
    ) -> None:
        super().__init__(web3_client=web3_client, slippage=slippage)

    def _get_pool_id(self, token: Token_Info):
        for token_address, info in contracts["stargate"]["pool_ids"][
            self.web3_client.network["name"]
        ].items():
            if token_address.lower() == token.address.lower():
                return info["id"]

    def _get_lz_fee(self, contract, dst: Token_Info, to_chain_id: int) -> Token_Amount:
        try:
            if dst.address == "":
                dst.address = "0x"
            data = (
                contract.functions.quoteLayerZeroFee(
                    to_chain_id,  # destination chainId
                    1,  # function type (1 - swap)
                    dst.address,  # destination of tokens
                    "0x",  # payload, using abi.encode()
                    [
                        0,  # extra gas, if calling smart contract
                        0,  # amount of dust dropped in destination wallet
                        "0x",  # destination wallet for dust
                    ],
                ).call(),
            )
            return Token_Amount(amount=data[0][0] * 1.05, wei=True)
        except Exception as error:
            return None

    def _execute_bridge(
        self,
        amount: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
        to_network: dict,
    ):
        from_pool_id = self._get_pool_id(token=from_token)
        to_pool_id = self._get_pool_id(token=from_token)
        to_chain_id = contracts["lz_chains_ids"][to_network["name"]]
        contract = self.web3_client.get_contract(
            address=contracts["stargate"]["router_contracts"][
                self.web3_client.network["name"]
            ],
            abi=contracts["stargate"]["router_abi"],
        )
        fee = self._get_lz_fee(contract=contract, dst=to_token, to_chain_id=to_chain_id)
        min_received_amount = Token_Amount(
            amount=amount.ether * 0.999,
            decimals=amount.decimals,
        )
        if from_token.symbol == "ETH":
            contract = self.web3_client.get_contract(
                address=contracts["stargate"]["router_contracts_eth"][
                    self.web3_client.network["name"]
                ],
                abi=contracts["stargate"]["router_abi_eth"],
            )
            args = (
                to_chain_id,
                self.web3_client.address,
                self.web3_client.address,
                amount.wei,
                min_received_amount.wei,
            )
            data = Web3Client.get_data_from_contrat(
                contract=contract, function_of_contract="swapETH", args=args
            )
            amount = Token_Amount(
                amount=amount.wei + fee.wei * 1.05,
                decimals=amount.decimals,
                wei=True,
            )
            return self.web3_client.send_transaction(
                from_token=from_token,
                to_address=contract.address,
                amount=amount,
                data=data,
            )
        else:
            args = (
                to_chain_id,  # destination chainId
                from_pool_id,  # source poolId
                to_pool_id,  # destination poolId
                self.web3_client.address,  # refund address. extra gas (if any) is returned to this address
                amount.wei,  # quantity to swap
                min_received_amount.wei,  # the min qty you would accept on the destination
                [
                    0,  # extra gas, if calling smart contract
                    0,  # amount of dust dropped in destination wallet
                    "0x",  # destination wallet for dust
                ],
                self.web3_client.address,  # the address to send the tokens to on the destination
                "0x",  # "fee" is the native gas to pay for the cross chain message fee
            )

            data = Web3Client.get_data_from_contrat(
                contract=contract, function_of_contract="swap", args=args
            )
            return self.web3_client.send_transaction(
                from_token=from_token,
                to_address=contract.address,
                amount=amount,
                data=data,
                value=fee,
            )
