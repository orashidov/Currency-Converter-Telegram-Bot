# extensions.py
import requests
import json

class APIException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CryptoConverter:
    def __init__(self, api_key, api_url="https://min-api.cryptocompare.com/data/price"):
        self.api_key = api_key
        self.api_url = api_url

    def get_price(self, base: str, quote: str, amount: str) -> float:
        try:
            response = requests.get(f'{self.api_url}?fsym={base}&tsyms={quote}&api_key={self.api_key}')
            response_data = json.loads(response.content)
            if 'Error' in response_data:
                raise APIException("Ошибка: неправильная или несуществующая валюта")
            return float(response_data[quote]) * float(amount)
        except Exception as e:
            raise APIException(f"Возникла непредвиденная ошибка: {repr(e)}")