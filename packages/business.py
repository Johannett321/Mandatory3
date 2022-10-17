from packages.product import Product

class Business:
    products = [Product(1, "Hey"), Product(2, "Halla")]

    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance

    def to_dict(self):
        products_dicts = {}
        for product in self.products:
            products_dicts.update(product.to_dict())
        print(str({"name": self.name, "balance": self.balance, "products": products_dicts}))
