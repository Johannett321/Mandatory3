import json

from packages.product import Product
from packages.storage_manager import write_string_to_file


class Business:
    products = []

    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance

    def add_product(self, product):
        self.products.append(product)

    def add_product_from_json(self, element):
        print(element["name"])
        print(element["stock"])
        self.add_product(Product(element["name"], element["stock"]))

    def product_exists(self, product_id):
        try:
            for product in self.products:
                if int(product.uid) == int(product_id):
                    return True
            return False
        except TypeError:
            print("Product ID should be a number")
            return False

    def get_product(self, product_id):
        try:
            for product in self.products:
                print(str(product_id) + " is not " + str(product.uid))
                if int(product.uid) == int(product_id):
                    return product
            return None
        except TypeError:
            print("Product ID should be a number")
            return None

    def sell_product(self, product_id):
        if self.product_exists(product_id):
            return self.get_product(product_id).sell(1)
        print("Could not find product with productID: " + product_id)
        return False

    def print_list_of_products(self):
        for product in self.products:
            print(str(product.uid) + ") " + product.name + " (Stock: " + str(product.stock) + ")")

    def to_dict(self):
        products_dicts = {}
        for product in self.products:
            products_dicts.update(product.to_dict())

        return {"name": self.name, "balance": self.balance, "products": products_dicts}

    def save(self):
        write_string_to_file("SaveFile.json", json.dumps(self.to_dict()))
        return True
