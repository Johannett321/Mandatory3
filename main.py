import os
import time

from packages.business import Business
from packages.product import Product
from packages.storage_manager import load_business_from_storage

business = load_business_from_storage()


def first_time_setup():
    global business
    business_name = input("Name of business: ")
    initial_balance = input("Initial balance: ")
    business = Business(business_name, initial_balance)
    business.save()
    print(business.to_dict())


def goto_menu_with_confirm():
    print("[PRESS ENTER TO CONTINUE]", end="")
    input()
    show_menu()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu(title=None, message=None):
    clear_console()
    if message is not None:
        print(title + ": " + message)
        print()
    print("--------------------- MENU ---------------------")
    print("1) About business")
    print("2) Manage products")
    chosen_command = input("Choose an option: ")

    if chosen_command.lower() == "1":
        print("---------------- ABOUT BUSINESS ----------------")
        print("Name: " + business.name)
        print("Balance: " + str(business.balance) + "kr")
        goto_menu_with_confirm()
    elif chosen_command.lower() == "2":
        manage_products()
    else:
        show_menu("Error", str(chosen_command) + " is not an option")


def manage_products():
    clear_console()
    print("---------------- MANAGE PRODUCTS ----------------")
    print("1) Add product")
    print("2) Remove product")
    print("3) Sell product")

    chosen_command = input("Choose an option: ")

    if chosen_command == "1":  # adding a product
        clear_console()
        print("------------------- ADD PRODUCT -------------------")

        # get info about product name and stock
        product_name = input("Product name: ")
        stock = input("Amount currently in stock: ")

        # make sure stock is a number
        try:
            int(stock)
        except ValueError:
            print("Stock is supposed to be a number. '" + stock + "' is not a number")
            manage_products()
            return

        # add the product and save
        business.add_product(Product(product_name, int(stock)))
        business.save()
        print()
        print("Product added!")
    elif chosen_command == "3": # selling a product
        clear_console()
        print("------------------ SELL PRODUCT ------------------")
        print("Please choose a product to sell:")
        business.print_list_of_products()
        product_to_sell = input("ProductID: ")
        if business.sell_product(product_to_sell) is False:
            manage_products()
            return
    else:  # unknown command
        print("Unknown command")
        time.sleep(1)
        manage_products()

    goto_menu_with_confirm()


if business is False:
    first_time_setup()

show_menu()
