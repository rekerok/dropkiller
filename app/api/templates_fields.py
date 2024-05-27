from flask_restful import fields


network = {
    "name": fields.String(attribute=lambda x: x["name"]),
    "short_name": fields.String(attribute=lambda x: x["short_name"]),
    "explorer": fields.String(attribute=lambda x: x["explorer"]),
    "chainId": fields.String(attribute=lambda x: x["chainId"]),
}

balance = {
    "wei": fields.Integer(attribute=lambda x: x.wei, default=0),
    "ether": fields.Float(attribute=lambda x: x.ether, default=0),
}

token = {
    "address": fields.String(attribute=lambda x: x.address),
    "symbol": fields.String(attribute=lambda x: x.symbol),
    "decimals": fields.String(attribute=lambda x: x.decimals),
}

balance_fields = {
    "address": fields.String(),
    "network": fields.Nested(network),
    "token": fields.Nested(token),
    "balance": fields.Nested(balance),
}

balances_fields = {
    "network": fields.Nested(network),
    "token": fields.Nested(token),
    "balances": fields.List(
        fields.Nested({"address": fields.String(), "balance": fields.Nested(balance)})
    ),
}

transaction = {
    "type": fields.String,
    "params": fields.Raw,
    "contract": fields.String,
    "address": fields.String,
    "amount": fields.Nested(balance),
}
transaction_full = {
    "transaction": fields.Nested(transaction),
    "network": fields.Nested(network),
}
