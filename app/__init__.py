from apispec import APISpec
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api
from app.api.dex import DexResource
from app.api.gas import GasNetworkResource
from app.api.ping import PingResource
from app.api.token import TokenResource
from app.config import *
from app.api.dexes import DexesResource
from apispec.ext.marshmallow import MarshmallowPlugin


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


# @app.route("/")
# def index():
#     return render_template("index.html")


@app.route("/api/ping")
def ping():
    return jsonify({"status": "you're in"})


### API
api.add_resource(GasNetworkResource, "/api/gas", endpoint="gas")
api.add_resource(DexResource, "/api/dex/<string:name>", endpoint="dex")
api.add_resource(DexesResource, "/api/dexes", endpoint="dexes")
api.add_resource(PingResource, "/api/ping", endpoint="ping")
api.add_resource(TokenResource, "/api/token", endpoint="token")

# DOCS
docs = FlaskApiSpec(app)
docs.register(GasNetworkResource, endpoint="gas")
docs.register(DexResource, endpoint="dex")
docs.register(DexesResource, endpoint="dexes")
docs.register(PingResource, endpoint="ping")
docs.register(TokenResource, endpoint="token")
