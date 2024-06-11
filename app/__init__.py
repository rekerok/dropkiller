from apispec import APISpec
from flask import Flask, render_template
from flask_apispec import FlaskApiSpec
from flask_restful import Api
from app.api.balance import BalanceResource
from app.api.bridge import BridgeResource
from app.api.dex import DexResource
from app.api.gas import GasNetworkResource
from app.api.ping import PingResource
from app.api.swap import SwapResource
from app.api.token import TokenResource
from app.api.transfer import TransferResource
from app.config import *
from app.api.dexes import DexesResource
from apispec.ext.marshmallow import MarshmallowPlugin

from app.utils.balance_utils import get_wallet_balances


app = Flask(__name__)
api = Api(app)
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="dropkiller API",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URL для Swagger JSON
        "APISPEC_SWAGGER_UI_URL": "/",  # URL для Swagger UI
    }
)


@app.route("/balance/<address>")
def balance_page(address):
    balances = get_wallet_balances(address)
    return render_template("balance.html", address=address, balances=balances)


### API
api.add_resource(GasNetworkResource, "/api/gas", endpoint="gas")
api.add_resource(DexResource, "/api/dex/<string:name>", endpoint="dex")
api.add_resource(DexesResource, "/api/dexes", endpoint="dexes")
api.add_resource(BalanceResource, "/api/balance/", endpoint="balance")
api.add_resource(PingResource, "/api/ping", endpoint="ping")
api.add_resource(TokenResource, "/api/token", endpoint="token")
api.add_resource(TransferResource, "/api/transfer", endpoint="transfer")
api.add_resource(SwapResource, "/api/swap", endpoint="swap")
api.add_resource(BridgeResource, "/api/bridge", endpoint="bridge")

# DOCS
docs = FlaskApiSpec(app)
docs.register(GasNetworkResource, endpoint="gas")
docs.register(DexResource, endpoint="dex")
docs.register(DexesResource, endpoint="dexes")
docs.register(BalanceResource, endpoint="balance")
docs.register(PingResource, endpoint="ping")
docs.register(TokenResource, endpoint="token")
docs.register(TransferResource, endpoint="transfer")
docs.register(SwapResource, endpoint="swap")
docs.register(BridgeResource, endpoint="bridge")
