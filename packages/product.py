import random


class Product:
    def __init__(self, name, stock):
        self.uid = random.randint(100000, 999999)
        self.name = name
        self.stock = stock
        print("Product created")

    def to_dict(self):
        return {self.uid: {"name": self.name, "stock": self.stock}}