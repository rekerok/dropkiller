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
    type=fields.Str(metadata={"description": "Type of the DEX"})


class DexesSchema(Schema):
    dexes = fields.List(
        fields.Nested(DexSchema), metadata={"description": "A list of DEXes"}
    )
