from flask_apispec import MethodResource, doc, marshal_with
from flask_restful import Resource
from app.api.shemas import DexesSchema
from app.models import get_network
from app.w3.swap import dex_swap
from app.w3.bridge import dex_bridge


class DexesResource(MethodResource, Resource):
    @doc(description="Get all DEXes and their supported networks", tags=["dexes "])
    @marshal_with(DexesSchema)  # Используем схему для сериализации ответа
    def get(self):
        # Собираем все DEX из двух источников
        all_dexes = list(dex_swap.values()) + list(dex_bridge.values())

        # Подготавливаем информацию для каждого DEX
        dex_info = [
            {
                "name": i.name,
                "url": i.url,
                "supported_networks": [
                    get_network(network) for network in i.support_networks
                ],
                "type": i.type,
            }
            for i in all_dexes
        ]

        # Оборачиваем список DEX в словарь под ключ 'dexes'
        return {"dexes": dex_info}
