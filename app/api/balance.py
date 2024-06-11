from flask_apispec import MethodResource, doc, marshal_with, use_kwargs
from flask_restful import Resource
from marshmallow import Schema, fields
from app.api.shemas import BalanceSchema
from app.models import get_network
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class BalanceResource(MethodResource, Resource):
    @doc(description="Get balance of a wallet", tags=["balance"])
    @use_kwargs(
        {
            "address": fields.Str(required=True, description="Wallet address"),
            "network": fields.Str(required=True, description="Network name"),
            "token_address": fields.Str(missing="", description="Token address"),
        },
        location="query",
    )
    @marshal_with(BalanceSchema)
    def get(self, address, network, token_address):
        network_data = get_network(name=network)
        w3 = Web3Client(network=network_data, address=address)
        token_info = Token_Info.get_info_token(
            w3_client=w3, token_address=token_address
        )
        balance = w3.get_balance(token_address=token_address)
        return {
            "address": address,
            "network": network_data,
            "token": token_info,
            "balance": balance,
        }
