import os

from packages.business_loader import get_business_from_menu
from packages.product import Product
from packages.storage_manager import load_string_from_file
from packages.tools import clear_console, press_enter_to_continue, maybe_exit

# change working dir to current
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

business_name = None
business = get_business_from_menu()


def goto_menu_with_confirm():
    press_enter_to_continue()
    show_menu()


def go_back_with_message(message: str, back):
    print(message)
    press_enter_to_continue()
    back()


def show_menu():
    clear_console()
    print("--------------------- MENU ---------------------")
    print("1) About business")
    print("2) Manage products")
    print("x) Exit")
    chosen_command = input("Choose an option: ").lower()

    if chosen_command == "1":
        clear_console()
        print("---------------- ABOUT BUSINESS ----------------")
        print("Name: " + business.name)
        print("Balance: " + str(business.balance) + "kr")
        goto_menu_with_confirm()
    elif chosen_command == "2":
        manage_products()
    elif chosen_command == "x":
        maybe_exit()
        show_menu()
        return
    else:
        print("'" + chosen_command + "' is not an option")
        goto_menu_with_confirm()


def manage_products():
    clear_console()
    print("---------------- MANAGE PRODUCTS ----------------")

    # menu options
    menu_items = [{"name": "Sell product", "function": sell_product},
                  {"name": "Check price", "function": check_price},
                  {"name": "Check stock", "function": check_stock},
                  {"name": "Add product", "function": add_product},
                  {"name": "Remove product", "function": delete_product},
                  {"name": "Restock product", "function": restock_product},
                  {"name": "Manage discounts", "function": manage_discounts},
                  {"name": "List all products with prices", "function": list_all_products_with_prices},
                  {"name": "List all transactions", "function": list_transactions}]

    # list all options
    for item_index in range(0, len(menu_items)):
        print(str(item_index + 1) + ") " + menu_items[item_index]["name"])

    # add go back option
    print("x) Go back")
    chosen_command = input("Choose: ").lower()

    # let user go back
    if chosen_command == "x":
        show_menu()
        return

    # make sure the user actually types something
    if chosen_command.isnumeric() is False or int(chosen_command) - 1 > len(menu_items):
        go_back_with_message("You must choose one of the options", manage_products)

    # launch menu option chosen by user
    menu_items[int(chosen_command) - 1]["function"]()


def sell_product():
    clear_console()
    print("------------------ SELL PRODUCT ------------------")
    print("Please choose a product to sell:")
    business.print_list_of_products()

    print()
    print("Type 'x' to cancel")

    # get productID
    product_to_sell = input("ProductID: ")

    # let the user exit
    if product_to_sell.lower() == "x":
        manage_products()
        return

    # make sure the product exists
    if business.product_exists(product_to_sell) is False:
        go_back_with_message("Could not find product with productID: " + product_to_sell, sell_product)
        return

    amount = input("Amount to sell: ")

    if amount.isnumeric() is not True:
        go_back_with_message("Amount must be a number: " + amount, sell_product)
        return

    if business.sell_product(product_to_sell, int(amount)) is False:
        press_enter_to_continue()
        manage_products()
        return
    business.save()

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def check_price():
    clear_console()
    print("------------------ CHECK PRICE ------------------")
    print("Please type the productID that you would like to check the price for:")
    print("You can also type 'x' to go back")
    product_id = input("ProductID: ").lower()

    if product_id == "x":
        manage_products()
        return

    if business.product_exists(product_id) is False:
        go_back_with_message("Could not find product with productID: " + product_id, check_price)
        return

    product = business.get_product(product_id)
    print(product.name + ": " + product.get_price_text())

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def check_stock():
    clear_console()
    print("------------------ CHECK STOCK ------------------")
    print("Please type the productID that you would like to check the stock for:")
    print("You can also type 'x' to go back")
    product_id = input("ProductID: ").lower()

    # let the user go back
    if product_id == "x":
        manage_products()
        return

    # make sure the product exists
    if business.product_exists(product_id) is False:
        go_back_with_message("Could not find product with productID: " + product_id, check_stock)
        return

    product = business.get_product(product_id)
    print(product.name + " in stock: " + str(product.stock))

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def add_product():
    clear_console()
    print("------------------- ADD PRODUCT -------------------")

    # get info about product name and stock
    print("You can also type 'x' to go back")
    product_name = input("Product name: ")
    if product_name == "x":
        manage_products()
        return
    if product_name == "":
        go_back_with_message("Product name cannot be empty", add_product)
        return

    stock = input("Amount currently in stock: ")
    if stock.isnumeric() is False:
        go_back_with_message("Stock must be a number", add_product)

    price = input("Selling price of item: ")
    if price.isnumeric() is False:
        go_back_with_message("Price must be a number", add_product)

    purchase_cost = input("Purchase cost for " + business.name + ": ")
    if purchase_cost.isnumeric() is False:
        go_back_with_message("Purchase cost must be a number", add_product)

    # add the product and save
    business.add_product(Product(product_name, int(stock), int(purchase_cost), int(price)))
    business.save()
    print("Product added!")

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def delete_product():
    clear_console()
    print("---------------- REMOVE PRODUCT ----------------")
    business.print_list_of_products()
    print()
    print("You can also type 'x' to go back")
    product_id = input("ProductID to delete: ")

    if product_id == "x":
        manage_products()
        return

    if business.product_exists(product_id) is False:
        go_back_with_message("Could not find product with productID: " + product_id, delete_product)

    if business.delete_product(product_id) is False:
        press_enter_to_continue()
        delete_product()

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def restock_product():
    clear_console()
    print("----------------- RESTOCK PRODUCT -----------------")
    print("Please choose a product to restock:")
    business.print_list_of_products()

    print()
    print("You can also type 'x' to go back")
    product_to_restock = input("ProductID: ")

    # let the user go back
    if product_to_restock == "x":
        manage_products()
        return

    if business.product_exists(product_to_restock) is False:
        go_back_with_message("Could not find product with productID: " + product_to_restock, restock_product)

    if business.get_product(product_to_restock) is None:
        go_back_with_message("Could not find product with productID: " + product_to_restock, restock_product)

    amount_to_restock = input("Amount to add to your warehouse: ")

    if amount_to_restock.isnumeric() is not True:
        go_back_with_message("Amount must be a number", restock_product)
        return

    if business.restock_product(product_to_restock, int(amount_to_restock)) is False:
        press_enter_to_continue()
        manage_products()
        return

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def list_all_products_with_prices():
    clear_console()
    print("----------------- ALL PRODUCTS -----------------")
    business.print_list_of_products()

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def list_transactions():
    print("------------------ TRANSACTIONS ------------------")
    transactions = load_string_from_file("transactions.txt")
    if transactions is None or transactions == "":
        print("There are no transactions for this business yet")
    else:
        print(transactions)

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


def manage_discounts():
    clear_console()
    print("-------------- MANAGE DISCOUNTS --------------")
    print("Please choose a product to manage discount's for")
    business.print_list_of_products()
    print()
    print("You can also type 'x' to go back")
    product_id = input("ProductID: ")
    print()

    # let user go back
    if product_id == "x":
        manage_products()
        return

    if business.product_exists(product_id) is False:
        go_back_with_message("Could not find product with productID: " + product_id, manage_discounts)

    print("Please choose an available option: ")
    if business.get_product(product_id).discounted_price is None:
        print("1) Add discount")
    else:
        print("1) Modify discount")
        print("2) Remove discount")

    print("x) Go back")
    chosen_option = input("Choose option: ").lower()

    if chosen_option.lower() == "x":
        manage_products()
        return

    if business.get_product(product_id).discounted_price is None:
        if chosen_option == "1":  # add discount
            discount_percent = input("Discount percent (without percentage symbol): ")
            if business.discount_product(product_id, int(discount_percent)) is False:
                press_enter_to_continue()
                manage_discounts()
                return
    else:
        if chosen_option == "1":  # modify discount
            discount_percent = input("New percent (without percentage symbol): ")
            if business.discount_product(product_id, int(discount_percent)) is False:
                press_enter_to_continue()
                manage_discounts()
                return
        elif chosen_option == "2":  # remove discount
            print("")

    # back to manage products menu
    press_enter_to_continue()
    manage_products()


show_menu()
