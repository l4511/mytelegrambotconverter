import json
import requests
from config import exchanges

class APIExceptions(Exception):
	pass

class Convertor:
	@staticmethod
	def get_price(amount , based , quote):
		try:
			based_key = exchanges[based.lower()]
		except KeyError:
			raise APIExceptions(f'Валюта {based} не найдена!')
		try:
			quote_key=exchanges[quote.lower()]
		except KeyError:
			raise APIExceptions(f'Валюта {quote} не найдена!')
		if based == quote:
                        raise APIExceptions(f'Невозможно перевести одинаковые валюты {quote}!')
		try:
			amount=float(amount)
		except ValueError:
			raise APIExceptions(f' Не удалось обработать количество {amount}!')

		r1=requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=6a33c02c840619281f83e2163509e6d8&base=EUR&symbols={based_key}')
		r2=requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=6a33c02c840619281f83e2163509e6d8&base=EUR&symbols={quote_key}')
		zapros1 = json.loads(r1.content)
		zapros2 = json.loads(r2.content)
		new_price1 = zapros1['rates'][based_key]
		new_price2 = zapros2['rates'][quote_key]
		new_price3=round((new_price2/new_price1)*amount,3)
		message = f'Цена {amount} {based_key} в {quote.lower()} : {new_price3}'
		return message

