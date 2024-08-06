#!/usr/bin/python

import sys
import os
import tty
import termios
import shutil  # For terminal size

ANSI_GREEN = "\033[92m"
ANSI_RESET = "\033[0m"

HOME = os.path.expanduser("~")
TODO_LIST_FOLDER = HOME + "/.py-todo/"
TODO_LIST_FILE = TODO_LIST_FOLDER + "todo.list"

def read_list():
    todo_list = []

    if not os.path.isdir(TODO_LIST_FOLDER):
        os.mkdir(TODO_LIST_FOLDER)

    if not os.path.isfile(TODO_LIST_FILE):
        open(TODO_LIST_FILE, "x").close()
    
    with open(TODO_LIST_FILE, "r") as file:
        while True:
            todo_item = file.readline().strip()
            properties = file.readline().strip()
            if not properties: 
                break
            properties_list = properties.split(',')
            assert(len(properties_list) == 2)
            assert((properties_list[0] == 'y' or properties_list[0] == 'n'))
            properties_obj = {"done" : properties_list[0], "rank" : properties_list[1]}
            todo_list.append([todo_item,properties_obj])

    return todo_list

TODO_LIST = read_list()

def sort():
    global TODO_LIST
    unsorted_list = TODO_LIST
    sorted_list = sorted(unsorted_list, key=lambda x: int(x[1]['rank']))
    TODO_LIST = sorted_list

def set_ranks():
    for i in range(0,len(TODO_LIST)):
        TODO_LIST[i][1]["rank"] = i

def add(name):
    TODO_LIST.append([name, {"done" : "n", "rank" : len(TODO_LIST)}])
    sort()
    set_ranks()

def remove(rank):
    TODO_LIST.pop(rank)
    sort()
    set_ranks()

def complete(rank):
    TODO_LIST[rank][1]["done"] = "y"
    sort()
    set_ranks()

def uncomplete(rank):
    TODO_LIST[rank][1]["done"] = "n"
    sort()
    set_ranks()

def clear():
    global TODO_LIST
    TODO_LIST = []

def save_list():
    with open(TODO_LIST_FILE, "w") as file:
        for item, properties in TODO_LIST:
            file.write(f"{item}\n")
            file.write(f"{properties['done']},{properties['rank']}\n")


USAGE = f"""{sys.argv[0]} <COMMAND>

Command     Meaning
list        Display the list
menu        Enter the menu
add         Enter the add menu (1 item)
remove      Enter the remove menu (1 item)
complete    Enter the complete menu (1 item)
uncomplete  Enter the uncomplete menu (1 item)
clear       Empty the todo list
"""

def as_num(string):
    try:
        x = int(string)
        return x
    except ValueError:
        return -1

def get_valid_rank():
    rank = -1
    while rank < 0 or rank >= len(TODO_LIST):
        rank_as_str = input("Enter number of item: ")
        rank = as_num(rank_as_str)
    return rank

def print_list():
    # Clear screen and print list
    os.system("clear")
    for i, (item, properties) in enumerate(TODO_LIST):
        status = "[X]" if properties["done"] == "y" else "[ ]"
        print(f"{i}. {status} {item}")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def menu_loop():
    global TODO_LIST
    quit_menu = False

    # Get terminal size
    terminal_size = shutil.get_terminal_size()
    term_width = terminal_size.columns
    term_height = terminal_size.lines

    while not quit_menu:
        print_list()
        sys.stdout.write('\033[?25l')  # Hide cursor
        
        # Calculate line position for menu
        menu_line = term_height - 1
        sys.stdout.write(f"\033[{menu_line};0H")  # Move cursor to bottom line
        
        # Print menu options
        menu_text = (
            f"{ANSI_GREEN}[A : add]{ANSI_RESET}, "
            f"{ANSI_GREEN}[R: remove]{ANSI_RESET}, "
            f"{ANSI_GREEN}[C : complete]{ANSI_RESET}, "
            f"{ANSI_GREEN}[U: uncomplete]{ANSI_RESET}, "
            f"[Q: quit]"
        )
        sys.stdout.write(menu_text)
        sys.stdout.flush()
        
        char = getch()
        match char:
            case "a" | "A":
                add(input("Enter item name: "))
            case "r" | "R":
                remove(get_valid_rank())
            case "c" | "C":
                complete(get_valid_rank())
            case "u" | "U":
                uncomplete(get_valid_rank())
            case "q" | "Q":
                quit_menu = True
                break
    sys.stdout.write('\033[?25h')  # Show cursor
    sys.stdout.flush()
    save_list()

def run_command(command):
    match command:
        case "list":
            print_list()
        case "menu":
            menu_loop()
        case "add":
            add(input("Enter item name: "))
            save_list()
        case "remove":
            remove(get_valid_rank())
            save_list()
        case "complete":
            complete(get_valid_rank())
            save_list()
        case "uncomplete":
            uncomplete(get_valid_rank())
            save_list()
        case "clear":
            clear()
            save_list()
        case _:
            print(USAGE)

if len(sys.argv) > 2:
    print(USAGE)
    exit(1)

if len(sys.argv) == 1:
    print_list()
else:
    run_command(sys.argv[1])
