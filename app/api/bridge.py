from flask_restful import Resource, reqparse, marshal_with
from loguru import logger
from app.models import get_network
from app.w3.web3_client import Web3Client
from . import templates_fields

# Создаем объект reqparse для обработки параметров запроса
parser = reqparse.RequestParser()
parser.add_argument("address", type=str, required=True)
parser.add_argument("from_network", type=str, required=True)
parser.add_argument("from_token_address", type=str, default="")
parser.add_argument("to_network", type=str, required=True)
parser.add_argument("to_token_address", type=str, default="")
parser.add_argument("amount", type=float)
parser.add_argument("dex", type=str, required=True)
parser.add_argument("slippage", type=int, default=5)


class Bridge(Resource):
    @marshal_with(templates_fields.transaction_full)
    def get(self):
        args = parser.parse_args()
        address = args["address"]
        from_network = get_network(name=args["from_network"])
        from_token_address = args["from_token_address"]
        to_network = get_network(name=args["to_network"])
        to_token_address = args["to_token_address"]
        amount = args["amount"]
        dex = args["dex"]

        w3_client = Web3Client(network=from_network, address=address)

        from app.w3.bridge import dex_bridge

        dex = dex_bridge[dex]
        dex = dex(web3_client=w3_client)
        transaction = dex.bridge(
            amount=amount,
            from_token_address=from_token_address,
            to_network=to_network,
            to_token_address=to_token_address,
        )
        return {"transaction": transaction, "network": from_network}
