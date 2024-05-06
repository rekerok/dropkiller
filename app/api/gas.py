from flask_restful import Resource

from app.models import get_networks
from app.w3.web3_client import Web3Client


class Gas(Resource):
    def get(self):
        gases = {}
        for network in get_networks():
            w3 = Web3Client(network=network)
            gases[network["name"]] = w3.get_gas()
        return gases, 200
