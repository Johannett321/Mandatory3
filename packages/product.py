import random


class Product:
    def __init__(self, name:str, stock:int):
        self.uid = random.randint(100000, 999999)
        self.name = name
        self.stock = stock
        print("Product created")

    def to_dict(self):
        return {self.uid: {"name": self.name, "stock": self.stock}}

    def sell(self, num_to_sell:int):
        if self.stock >= num_to_sell:
            self.stock -= num_to_sell
            print("Sold product: " + self.name)
            return True
        print("Product is out of stock. Could not sell product")
        return False
