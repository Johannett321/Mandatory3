from packages.warehouse import *
from packages.storage_manager import *
from packages.business import *


def read_cmd():
    command = input("Command: ")
    command_parts = command.split(" ")
    if command_parts[0] == "product":
        if command_parts[1] == "add":
            print("Added product")

    read_cmd()


def run_setup():
    print("Running setup")
    business_name = input("Name of business: ")
    initial_balance = input("Initial balance (money): ")
    business = Business(business_name, initial_balance)
    save_business(business)


if load_data() is False:
    print("No data could be found")
    run_setup()
    exit(0)

read_cmd()
