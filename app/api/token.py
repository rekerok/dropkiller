from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from marshmallow import fields

from app.api.shemas import TokenSchema
from app.models import get_network
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class TokenResource(MethodResource):
    @doc(description="Get token information via query parameters", tags=["token"])
    @use_kwargs(
        {
            "network": fields.Str(required=True, description="Network name"),
            "token_address": fields.Str(
                required=False, missing="", description="Token address"
            ),
        },
        location="query",
    )
    @marshal_with(TokenSchema)  # Используем схему для сериализации ответа
    def get(self, network, token_address):
        # Пример: получение данных из сети и расчет информации о токене
        network_data = get_network(name=network)
        w3 = Web3Client(network=network_data)
        token_info = Token_Info.get_info_token(
            w3_client=w3, token_address=token_address
        )
        result = {
            "symbol": token_info.symbol,
            "address": token_info.address,
            "decimals": token_info.decimals,
        }
        return result, 200
