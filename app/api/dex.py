import pprint
from flask_restful import Resource, reqparse, marshal_with
from app.models import get_network
from app.w3.swap import dex_swap
from app.w3.bridge import dex_bridge
from flask import jsonify
from . import templates_fields


class Dexex(Resource):
    @marshal_with(templates_fields.dexes)
    def get(self):
        # Собираем все DEX из двух источников
        all_dexes = list(dex_swap.values()) + list(dex_bridge.values())

        # Подготавливаем информацию для каждого DEX
        dex_info = [
            {
                "name": i.NAME,
                "url": i.URL,
                "supported_networks": [
                    get_network(network) for network in i.SUPPORT_NETWORKS
                ],
            }
            for i in all_dexes
        ]

        # Оборачиваем список DEX в словарь под ключ 'dexes'
        # pprint.pprint(dex_info)
        return {"dexes": dex_info}
