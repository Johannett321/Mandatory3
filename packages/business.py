import json
from datetime import datetime

from packages.product import Product
from packages.storage_manager import write_string_to_file, load_string_from_file
from packages.tools import money_text, strike_text


class Business:
    products = []

    def __init__(self, name, initial_balance: int):
        self.name = name
        self.balance = initial_balance

    def add_product(self, product):
        self.products.append(product)

    def add_product_from_json(self, element):
        self.add_product(Product(element["name"], element["stock"],
                                 element["purchase_cost"], element["price"],
                                 element["discounted_price"]))

    def delete_product(self, product_id):
        product = self.get_product(product_id)
        if product is None:
            print("Could not find product with productID: " + product_id)
            return False
        self.products.remove(product)
        print(product.name + " was deleted!")
        self.save()
        return True

    def product_exists(self, product_id):
        try:
            for product in self.products:
                if int(product.uid) == int(product_id):
                    return True
            return False
        except TypeError:
            print("Product ID should be a number")
            return False
        except ValueError:
            print("Could not find product")
            return False

    def get_product(self, product_id):
        try:
            for product in self.products:
                if int(product.uid) == int(product_id):
                    return product
            return None
        except TypeError:
            print("Product ID should be a number")
            return None

    def sell_product(self, product_id, amount_to_sell: int):
        if self.product_exists(product_id):
            product = self.get_product(product_id)
            if amount_to_sell > product.stock:
                print(self.name + " does not have " + str(amount_to_sell) + " " + product.name +
                      " in stock. Current stock: " + str(product.stock))
                return False

            sold_for = product.discounted_price
            if sold_for is None:
                sold_for = product.price
            self.balance += sold_for*amount_to_sell
            self.add_row_to_transactions("Sold " + str(amount_to_sell) + " " + product.name +
                                         " for " + money_text(sold_for))
            return product.sell(amount_to_sell)
        print("Could not find product with productID: " + product_id)
        return False

    def restock_product(self, product_id, amount: int):
        product = self.get_product(product_id)
        total_purchase_cost = product.purchase_cost * amount

        # check if business has enough money
        if total_purchase_cost > self.balance:
            print(self.name + " cannot afford to buy " + str(amount) + " " + product.name
                  + " for " + money_text(total_purchase_cost) + " as "
                  + self.name + " only has " + money_text(self.balance) + " in it's account")
            return False

        self.balance -= total_purchase_cost
        product.restock(amount)
        print(self.name + " puchased " + str(amount) + " " + product.name + " for " + money_text(total_purchase_cost) +
              ". " + self.name + "'s new balance is: " + money_text(self.balance))
        self.save()
        return True

    def discount_product(self, product_id, discount_percentage: int):
        if self.product_exists(product_id):
            if discount_percentage >= 100 or discount_percentage <= 0:
                print("Discount percentage must be a number greater than 0, and less than 100")
                return False
            product = self.get_product(product_id)
            product.add_discount(discount_percentage)
            print(product.name + " just got discounted! Old price: " + strike_text(money_text(product.price)) +
                  ". New price: " + money_text(product.discounted_price))
            self.save()
            return True
        else:
            return False

    def print_list_of_products(self):
        for product in self.products:
            print(str(product.uid) + ") " + product.name + " (Stock: " + str(
                product.stock) + ", Price: " + product.get_price_text() + ")")
        if len(self.products) == 0:
            print("There are no products yet")

    def add_row_to_transactions(self, row:str):
        current_date = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

        current_transaction_log = load_string_from_file("transactions.txt")
        if current_transaction_log is not None and current_transaction_log != "":
            current_transaction_log += "\n"
        elif current_transaction_log is None:
            current_transaction_log = ""
        current_transaction_log += current_date + ": " + row

        write_string_to_file("transactions.txt", current_transaction_log)

    def to_dict(self):
        products_dicts = {}
        for product in self.products:
            products_dicts.update(product.to_dict())

        return {"name": self.name, "balance": self.balance, "products": products_dicts}

    def save(self):
        write_string_to_file("SaveFile.json", json.dumps(self.to_dict()))
        return True
