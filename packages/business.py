import json

from packages.product import Product
from packages.storage_manager import write_string_to_file


class Business:
    products = [Product(1, "Hey"), Product(2, "Halla")]

    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance

    def to_dict(self):
        products_dicts = {}
        for product in self.products:
            products_dicts.update(product.to_dict())

        return {"name": self.name, "balance": self.balance, "products": products_dicts}

    def save(self):
        write_string_to_file("SaveFile.json", json.dumps(self.to_dict()))
        return True
