from marshmallow import Schema, fields


class CurrencySchema(Schema):
    name = fields.Str(metadata={"description": "The name of the currency"})
    decimals = fields.Int(
        metadata={"description": "The number of decimals for the currency"}
    )


class NetworkSchema(Schema):
    name = fields.Str(metadata={"description": "The name of the network"})
    short_name = fields.Str(metadata={"description": "The short name of the network"})
    explorer = fields.Str(metadata={"description": "The explorer URL of the network"})
    chainId = fields.Int(metadata={"description": "The chain ID of the network"})
    url = fields.Str(metadata={"description": "The URL of the network"})
    currency = fields.Nested(
        CurrencySchema, metadata={"description": "The currency details of the network"}
    )


class GasNetworkSchema(Schema):
    network = fields.Nested(
        NetworkSchema, metadata={"description": "The network details"}
    )
    gas = fields.Float(metadata={"description": "The current gas price"})


class DexSchema(Schema):
    name = fields.Str(metadata={"description": "The name of the DEX"})
    url = fields.Str(metadata={"description": "The URL of the DEX"})
    supported_networks = fields.List(
        fields.Nested(NetworkSchema),
        metadata={"description": "The supported networks of the DEX"},
    )
    type = fields.Str(metadata={"description": "Type of the DEX"})


class DexesSchema(Schema):
    dexes = fields.List(
        fields.Nested(DexSchema), metadata={"description": "A list of DEXes"}
    )


class AmountSchema(Schema):
    wei = fields.Integer(metadata={"description": "Balance in wei"}, default=0)
    ether = fields.Float(metadata={"description": "Balance in ether"}, default=0)
    decimals = fields.Integer(metadata={"description": "Balance decimals"})


class TokenSchema(Schema):
    symbol = fields.Str(metadata={"description": "Token symbol"})
    address = fields.Str(metadata={"description": "Token address"})
    decimals = fields.Integer(metadata={"description": "Token decimals"})


class BalanceSchema(Schema):
    address = fields.Str(metadata={"description": "Wallet address"})
    network = fields.Nested(NetworkSchema, metadata={"description": "Network details"})
    token = fields.Nested(TokenSchema, metadata={"description": "Token details"})
    balance = fields.Nested(
        AmountSchema, metadata={"description": "Balance amount details"}
    )


class TransactionSchema(Schema):
    type = fields.Str()
    params = fields.Dict()
    contract = fields.Str()
    address = fields.Str()
    amount = fields.Nested(AmountSchema)


class TransferSchema(Schema):
    transaction = fields.Nested(TransactionSchema)
    network = fields.Nested(NetworkSchema)


class SwapSchema(Schema):
    transaction = fields.Nested(TransactionSchema)
    network = fields.Nested(NetworkSchema)
    from_token = fields.Nested(TokenSchema)
    to_token = fields.Nested(TokenSchema)


class BridgeSchema(Schema):
    transaction = fields.Nested(TransactionSchema)
    from_network = fields.Nested(NetworkSchema)
    to_network = fields.Nested(NetworkSchema)
    from_token = fields.Nested(TokenSchema)
    to_token = fields.Nested(TokenSchema)
