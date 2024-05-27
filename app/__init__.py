from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import *
from app.api.approve import Approve
from app.api.gas import Gas
from app.api.balance import Balance
from app.api.swap import Swap
from app.api.token import Token
from app.api.transfer import Transfer
from app.api.bridge import Bridge


app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return "Hello, world!"


### SWAGGER SETTINGS
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_API_URL, SWAGGER_FILE, config={"name": "dropkiller.app"}
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_API_URL)

### API
api.add_resource(Gas, "/api/gas", endpoint="gas")
api.add_resource(Balance, "/api/balance", endpoint="balance")
api.add_resource(Token, "/api/token", endpoint="token")
api.add_resource(Swap, "/api/swap", endpoint="swap")
api.add_resource(Approve, "/api/approve", endpoint="approve")
api.add_resource(Transfer, "/api/transfer", endpoint="transfer")
api.add_resource(Bridge, "/api/bridge", endpoint="bridge")
