from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from marshmallow import fields

from app.api.shemas import BridgeSchema
from app.models import get_network
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class BridgeResource(MethodResource):
    @doc(description="Bridge tokens between networks using a DEX", tags=["bridge"])
    @use_kwargs(
        {
            "address": fields.Str(required=True, description="Wallet address"),
            "from_network": fields.Str(required=True, description="From network name"),
            "from_token_address": fields.Str(
                required=False, missing="", description="From token address"
            ),
            "to_network": fields.Str(required=True, description="To network name"),
            "to_token_address": fields.Str(
                required=False, missing="", description="To token address"
            ),
            "amount": fields.Float(required=True, description="Amount to bridge"),
            "dex": fields.Str(required=True, description="DEX name"),
            "slippage": fields.Int(
                required=False, missing=5, description="Slippage percentage"
            ),
        },
        location="query",
    )
    @marshal_with(BridgeSchema)
    def get(
        self,
        address,
        from_network,
        from_token_address,
        to_network,
        to_token_address,
        amount,
        dex,
        slippage,
    ):
        from_network_data = get_network(name=from_network)
        to_network_data = get_network(name=to_network)
        w3_client = Web3Client(network=from_network_data, address=address)
        from_token = Token_Info.get_info_token(
            w3_client=w3_client, token_address=from_token_address
        )
        to_token = Token_Info.get_info_token(
            w3_client=Web3Client(network=to_network_data, address=address),
            token_address=to_token_address,
        )
        from app.w3.bridge import dex_bridge

        dex = dex_bridge[dex](web3_client=w3_client, slippage=slippage)
        transaction = dex.bridge(
            amount=amount,
            from_token_address=from_token_address,
            to_network=to_network_data,
            to_token_address=to_token_address,
        )
        return {
            "transaction": transaction,
            "from_network": from_network_data,
            "to_network": to_network_data,
            "from_token": from_token,
            "to_token": to_token,
        }
