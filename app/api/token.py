from flask_restful import Resource, reqparse, marshal_with

from app import w3
from app.models import get_network
from app.w3.token_info import Token_Info
from . import templates_fields

parser = reqparse.RequestParser()
parser.add_argument("network", type=str, default="ethereum")
parser.add_argument("token_address", type=str, default="")


class Token(Resource):
    @marshal_with(templates_fields.token)
    def get(self):
        args = parser.parse_args()
        network = get_network(name=args["network"])
        token_address = args["token_address"]
        w3 = w3.Web3Client(network=network)
        token_info = Token_Info.get_info_token(
            w3_client=w3, token_address=token_address
        )
        return token_info
