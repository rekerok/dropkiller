from flask_restful import Resource, reqparse, marshal_with

from app.models import get_network
from app.w3.web3_client import Web3Client
from . import templates_fields

# Создаем объект reqparse для обработки параметров запроса
parser = reqparse.RequestParser()
parser.add_argument("address", type=str, required=True)
parser.add_argument("network", type=str, default="ethereum")
parser.add_argument("from_token_address", type=str, default="")
parser.add_argument("to_token_address", type=str, default="")
parser.add_argument("amount", type=int)
parser.add_argument("dex", type=str, required=True)
parser.add_argument("slippage", type=int, default=5)


class Swap(Resource):
    @marshal_with(templates_fields.transaction_full)
    def get(self):
        args = parser.parse_args()
        address = args["address"]
        network = get_network(name=args["network"])
        from_token_address = args["from_token_address"]
        to_token_address = args["to_token_address"]
        amount = float(args["amount"])
        dex = args["dex"]
        w3_client = Web3Client(network=network, address=address)

        from app.w3.swap import dex_swap

        dex = dex_swap[dex]

        dex = dex(web3_client=w3_client)
        transaction = dex.swap(
            amount=10,
            from_token_address=from_token_address,
            to_token_address=to_token_address,
        )
        return {"transaction": transaction, "network": network}
