from flask_apispec import MethodResource, doc, marshal_with
from flask_restful import Resource
from app.api.shemas import DexSchema, DexesSchema
from app.models import get_network
from app.w3.swap import dex_swap
from app.w3.bridge import dex_bridge


class DexResource(MethodResource, Resource):
    @doc(description="Get all DEXes and their supported networks", tags=["dexes "])
    @marshal_with(DexSchema)  # Используем схему для сериализации ответа
    def get(self, name):
        # Собираем все DEX из двух источников
        all_dexes = {**dex_swap, **dex_bridge}
        dex = all_dexes.get(name)
        print(dex)
        # Подготавливаем информацию для каждого DEX
        dex_info = {
            "name": dex.name,
            "url": dex.url,
            "supported_networks": [
                get_network(network) for network in dex.support_networks
            ],
            "type": dex.type,
        }
        # Оборачиваем список DEX в словарь под ключ 'dexes'
        return dex_info
