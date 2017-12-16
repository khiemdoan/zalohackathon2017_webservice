# coding=utf-8

import os
try:
    import simplejson as json
except ImportError:
    import json
from redis import Redis


class Product:

    def __init__(self):
        self._cache = Redis()
        if self._cache.hlen('products') > 0:
            return

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'database.json')
        try:
            with open(file_path, 'r') as infile:
                data = json.load(infile)
                for product in data:
                    self._cache.hset('products', product['productId'], json.dumps(product))
                    number = self._cache.hget('categories', product['category'])
                    if number is None:
                        number = 0
                    number = int(number)
                    self._cache.hset('categories', product['category'], number + 1)
                    self._cache.hset(product['category'], product['productId'], json.dumps(product))
        except:
            pass

    def get_all(self):
        product_dict = self._cache.hgetall('products')
        products = [product for product_id, product in product_dict.items()]
        return [json.loads(product) for product in products]

    def get_by_category(self, category):
        product_dict = self._cache.hgetall(category)
        products = [product for product_id, product in product_dict.items()]
        return [json.loads(product) for product in products]

    def find(self, product_id=''):
        product_str = self._cache.hget('products', product_id)
        try:
            return json.loads(product_str)
        except:
            return None

    def get_categories(self):
        return self._cache.hkeys('categories')
