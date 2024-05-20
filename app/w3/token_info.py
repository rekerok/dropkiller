import eth_utils
from app.models import contracts


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
                    address=token_address, abi=contracts["erc20_abi"]
                )
                symbol = contract.functions.symbol().call()
                decimals = contract.functions.decimals().call()
            return Token_Info(
                address=address,
                symbol=symbol.upper(),
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
