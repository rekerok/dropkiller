from app.models import get_networks
from app.w3.web3_client import Web3Client
from app.w3.token_info import Token_Info


def get_wallet_balances(address):
    balances = {}
    networks = get_networks()
    for network in networks:
        network_name = network["name"]
        balances[network_name] = {}
        w3 = Web3Client(network=network, address=address)
        tokens = network.get("tokens", [])
        for token_address in tokens:
            token_info = Token_Info.get_info_token(
                w3_client=w3, token_address=token_address
            )
            balance = w3.get_balance(token_address=token_address)
            balances[network_name][token_info.symbol] = balance.ether
    return balances
