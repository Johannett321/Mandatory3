import os

debug_mode = False


def strike_text(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


def money_text(money: int):
    return str(money) + " kr"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def press_enter_to_continue():
    print("[PRESS ENTER TO CONTINUE]", end="")
    input()

def maybe_exit():
    sure = input("Sure? (y/n)").lower()
    if sure == "y":
        exit(0)