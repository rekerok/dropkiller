from flask_apispec import MethodResource, doc, marshal_with
from app.api.shemas import GasNetworkSchema
from app.models import get_networks
from app.w3.web3_client import Web3Client


class GasNetworkResource(MethodResource):
    @doc(
        description="Get current gas prices and network details for all networks",
        tags=["gas"],
    )
    @marshal_with(
        GasNetworkSchema(many=True)
    )  # Используем схему для сериализации ответа
    def get(self):
        result = []
        for network in get_networks():
            w3 = Web3Client(network=network)
            gas_data = {
                "network": {
                    "name": network["name"],
                    "short_name": network["short_name"],
                    "explorer": network["explorer"],
                    "eip1559": network["eip1559"],
                    "chainId": network["chainId"],
                    "rpc": network["rpc"],
                    "url": network["url"],
                    "currency": {
                        "name": network["currency"]["name"],
                        "decimals": network["currency"]["decimals"],
                    },
                },
                "gas": w3.get_gas(),
            }
            result.append(gas_data)
        return result, 200
