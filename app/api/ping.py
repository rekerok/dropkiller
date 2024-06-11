from flask import jsonify
from flask_apispec import MethodResource, doc


class PingResource(MethodResource):
    @doc(description="Check server status", tags=["utils"])
    def get(self):
        return {"status": "you're in"}, 200
