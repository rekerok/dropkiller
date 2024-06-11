from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from marshmallow import fields

from app.api.shemas import TransferSchema
from app.models import get_network
from app.w3.web3_client import Web3Client


class TransferResource(MethodResource):
    @doc(description="Transfer tokens between addresses", tags=["transfer"])
    @use_kwargs(
        {
            "from_address": fields.Str(required=True, description="Sender address"),
            "to_address": fields.Str(required=True, description="Recipient address"),
            "network": fields.Str(required=True, description="Network name"),
            "token_address": fields.Str(
                required=False, missing="", description="Token address"
            ),
            "amount": fields.Float(required=True, description="Amount to transfer"),
        },
        location="query",
    )
    @marshal_with(TransferSchema)
    def get(self, from_address, to_address, network, token_address, amount):
        network_data = get_network(name=network)
        w3_client = Web3Client(network=network_data, address=from_address)

        transaction = w3_client.transfer(
            to_address=to_address, amount=amount, token_address=token_address
        )
        return {"transaction": transaction, "network": network_data}
