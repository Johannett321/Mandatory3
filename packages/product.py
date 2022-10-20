import random

from packages.tools import strike_text


class Product:
    def __init__(self, name: str, stock: int, purchase_cost: int, price: int, discounted_price: int = None):
        self.uid = random.randint(100000, 999999)
        self.name = name
        self.purchase_cost = purchase_cost
        self.price = price
        self.discounted_price = discounted_price
        self.stock = stock

    def to_dict(self):
        return {self.uid: {"name": self.name,
                           "stock": self.stock,
                           "purchase_cost": self.purchase_cost,
                           "price": self.price,
                           "discounted_price": self.discounted_price}}

    def add_discount(self, percentage: int):
        self.discounted_price = self.price - self.price * (percentage / 100)

    def remove_discount(self):
        self.discounted_price = None

    def get_price(self):
        if self.discounted_price is not None:
            return self.discounted_price
        else:
            return self.price

    def get_price_text(self):
        if self.discounted_price is not None:
            return strike_text(str(self.price) + " kr") + " " + str(self.discounted_price) + " kr"
        return str(self.price) + " kr"

    def sell(self, num_to_sell: int):
        if self.stock >= num_to_sell:
            self.stock -= num_to_sell
            print("Sold product: " + self.name)
            return True
        print("Product is out of stock. Could not sell product")
        return False

    def restock(self, amount_to_add):
        self.stock += amount_to_add
