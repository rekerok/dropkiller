from flask import Flask
from flask_restful import Api

from app.api.approve import Approve
from app.api.gas import Gas
from app.api.balance import Balance
from app.api.swap import Swap
from app.api.token import Token
from app.api.transfer import Transfer


app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return "Hello, world!"


api.add_resource(Gas, "/api/gas", endpoint="gas")
api.add_resource(Balance, "/api/balance", endpoint="balance")
api.add_resource(Token, "/api/token", endpoint="token")
api.add_resource(Swap, "/api/swap", endpoint="swap")
api.add_resource(Approve, "/api/approve", endpoint="approve")
api.add_resource(Transfer, "/api/transfer", endpoint="transfer")
