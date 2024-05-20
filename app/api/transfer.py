from flask_restful import Resource, reqparse, marshal_with

from app.models import get_network
from app.w3.web3_client import Web3Client
from . import templates_fields

# Создаем объект reqparse для обработки параметров запроса
parser = reqparse.RequestParser()
parser.add_argument("from_address", type=str, required=True)
parser.add_argument("to_address", type=str, required=True)
parser.add_argument("network", type=str, required=True)
parser.add_argument("token_address", type=str, default="")
parser.add_argument("amount", type=int)


class Transfer(Resource):
    @marshal_with(templates_fields.transaction_full)
    def get(self):
        args = parser.parse_args()
        from_address = args["from_address"]
        to_address = args["to_address"]
        network = get_network(name=args["network"])
        token_address = args["token_address"]
        amount = float(args["amount"])
        w3_client = Web3Client(network=network, address=from_address)

        transaction = w3_client.transfer(
            to_address=token_address, amount=10, token_address=token_address
        )
        return {"transaction": transaction, "network": network}
