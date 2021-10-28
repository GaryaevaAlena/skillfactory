import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f'Валюта {base} не найдена')
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            return APIException(f'Валюта {quote} не найдена')

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}&api_key=a94efa0350079477068e7f5d2ae4e7c2b3dbd85321a04b45056dc26ab2c665c3")
        resp = json.loads(r.content)
        new_price = resp[quote_key] * float(amount)
        return round(new_price, 2)

