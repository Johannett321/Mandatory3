import os

from packages.business import Business
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
    else:
        show_menu("Error", str(chosen_command) + " is not an option")


if business is False:
    first_time_setup()

show_menu()
