from flask_restful import Resource, marshal_with, reqparse

from app import w3
from app.models import get_network
from app.w3.token_info import Token_Info
from . import templates_fields

parser = reqparse.RequestParser()
parser.add_argument("address", type=str, required=True)
parser.add_argument("network", type=str)
parser.add_argument("token_address", type=str, default="")


class Balance(Resource):
    @marshal_with(templates_fields.balance_fields)
    def get(self):
        args = parser.parse_args()
        address = args["address"]
        network = get_network(name=args["network"])
        token_address = args["token_address"]
        w3 = w3.Web3Client(network=network, address=address)
        token_info = Token_Info.get_info_token(
            w3_client=w3, token_address=token_address
        )
        balance = w3.get_balance(token_address=token_address)
        return {
            "address": address,
            "network": network,
            "token": token_info,
            "balance": balance,
        }
