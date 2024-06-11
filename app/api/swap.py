from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from marshmallow import fields
from app.api.shemas import SwapSchema
from app.models import get_network
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client


class SwapResource(MethodResource):
    @doc(description="Swap tokens using a DEX", tags=["swap"])
    @use_kwargs(
        {
            "address": fields.Str(required=True, description="Wallet address"),
            "network": fields.Str(required=True, description="Network name"),
            "from_token_address": fields.Str(
                required=False, missing="", description="From token address"
            ),
            "to_token_address": fields.Str(
                required=False, missing="", description="To token address"
            ),
            "amount": fields.Float(required=True, description="Amount to swap"),
            "dex": fields.Str(required=True, description="DEX name"),
            "slippage": fields.Int(
                required=False, missing=5, description="Slippage percentage"
            ),
        },
        location="query",
    )
    @marshal_with(SwapSchema)
    def get(
        self,
        address,
        network,
        from_token_address,
        to_token_address,
        amount,
        dex,
        slippage,
    ):
        network_data = get_network(name=network)
        w3_client = Web3Client(network=network_data, address=address)
        from_token = Token_Info.get_info_token(
            w3_client=w3_client, token_address=from_token_address
        )
        to_token = Token_Info.get_info_token(
            w3_client=w3_client, token_address=to_token_address
        )
        from app.w3.swap import dex_swap

        dex = dex_swap[dex]

        dex = dex(web3_client=w3_client)
        transaction = dex.swap(
            amount=amount,
            from_token_address=from_token_address,
            to_token_address=to_token_address,
        )
        return {
            "transaction": transaction,
            "network": network,
            "from_token": from_token,
            "to_token": to_token,
        }
