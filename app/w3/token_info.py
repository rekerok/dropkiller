import eth_utils
from app.abis import abis


class Token_Info:
    def __init__(self, address, symbol, decimals):
        self.address: str = address
        self.symbol: str = symbol
        self.decimals: int = decimals

    @staticmethod
    def get_info_token(w3_client, token_address: str = None):
        try:
            if not token_address or token_address == "":
                address = ""
                symbol: str = w3_client.network["currency"]["name"].upper()
                decimals: int = int(w3_client.network["currency"]["decimals"])
            else:
                address = eth_utils.address.to_checksum_address(token_address)
                contract = w3_client.get_contract(
                    address=token_address, abi=abis["erc20"]
                )
                symbol = contract.functions.symbol().call().upper()
                decimals = contract.functions.decimals().call()
            return Token_Info(
                address=address,
                symbol=symbol,
                decimals=decimals,
            )
        except Exception as error:
            return None

    @staticmethod
    def is_native_token(network: dict, token: "Token_Info"):
        return (
            True
            if token.symbol.upper() == network["currency"]["name"].upper()
            else False
        )

    # @staticmethod
    # async def to_wrapped_token(
    #     network: config.Network,
    #     from_token: "Token_Info" = None,
    #     to_token: "Token_Info" = None,
    # ):
    #     if from_token:
    #         if from_token.address == "":
    #             from_token.address = eth_utils.address.to_checksum_address(
    #                 config.GENERAL.WETH.get(network.get(NETWORK_FIELDS.NAME))
    #             )
    #     if to_token:
    #         if to_token.address == "":
    #             to_token.address = eth_utils.address.to_checksum_address(
    #                 config.GENERAL.WETH.get(network.get(NETWORK_FIELDS.NAME))
    #             )
    #     return from_token, to_token

    # @staticmethod
    # async def to_native_token(
    #     from_token: "Token_Info" = None,
    #     to_token: "Token_Info" = None,
    # ):
    #     if from_token:
    #         if from_token.address == "":
    #             from_token.address = eth_utils.address.to_checksum_address(
    #                 config.GENERAL.NATIVE_TOKEN
    #             )
    #     if to_token:
    #         if to_token.address == "":
    #             to_token.address = eth_utils.address.to_checksum_address(
    #                 config.GENERAL.NATIVE_TOKEN
    #             )
    #     return from_token, to_token
