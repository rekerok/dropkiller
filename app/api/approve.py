from flask_restful import Resource, reqparse, marshal_with

from app.models import get_network
from app.w3.token_amount import Token_Amount
from app.w3.token_info import Token_Info
from app.w3.web3_client import Web3Client
from . import templates_fields

# Создаем объект reqparse для обработки параметров запроса
parser = reqparse.RequestParser()
parser.add_argument("network", type=str)
parser.add_argument("token_address", type=str)
parser.add_argument("owner", type=str)
parser.add_argument("spender", type=str)
parser.add_argument("amount", type=float)


class Approve(Resource):
    @marshal_with(templates_fields.transaction_full)
    def get(self):
        args = parser.parse_args()
        network = get_network(name=args["network"])
        owner = args["owner"]
        token_address = args["token_address"]
        spender = args["spender"]
        amount = float(args["amount"])
        w3_client = Web3Client(network=network, address=owner)

        token_info = Token_Info.get_info_token(
            w3_client=w3_client, token_address=token_address
        )
        amount = Token_Amount(amount=amount, decimals=token_info.decimals)
        params = w3_client.get_data_for_approve(
            token=token_info, spender=spender, amount=amount
        )
        transaction = {
            "type": "approve",
            "params": params,
            "contract": token_info.address,
            "address": w3_client.address,
            "amount": Token_Amount(amount=0),
        }
        return {"transaction": transaction, "network": network}
