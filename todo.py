#!/usr/bin/python
import os
import sys


GREEN = '\033[32m'
RESET = '\033[0m'
home = os.path.expanduser("~")
todo_list = []
example_list = [["Walk dog", {"done" : "n", "rank": 0}], ["Walk cat", {"done" : "y", "rank": 1}]]

def write_list():
    with open(f"{home}/.pytodo/todo.list", "w") as f:
        for item in todo_list:
            f.write(item[0] + "\n")
            f.write(f"{item[1]['done']},{item[1]['rank']}\n")

def read_list():
    with open(f"{home}/.pytodo/todo.list", "r") as f:
        while True:
            todo_item = f.readline().strip()
            properties = f.readline().strip()
            if not properties: 
                break
            properties_list = properties.split(',')
            properties_obj = {"done" : properties_list[0], "rank" : properties_list[1]}
            todo_list.append([todo_item,properties_obj])

def display_list():
    i = 0
    sorted_list = sorted(todo_list, key=lambda x: int(x[1]['rank']))
    for entry in sorted_list:
        done = False if entry[1]["done"] == 'n' else True
        print(f"{GREEN if done else ""}{i}. [{"X" if done else " "}] {entry[0]}{RESET}")
        i+=1


def print_usage():
    print("USAGE")

def add_item(name: ""):
    if name == "":
        name = input("Enter name of item: ")
    todo_list.append([name, {"done": "n", "rank": len(todo_list)}])
    return

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def select_item(string):
    index = input(string)
    if not is_int(index):
        print("Not a number!")
        return -1
    i = int(index)
    if i >= len(todo_list) or i < 0:
        print("Invalid selection!")
        return -1

def complete_item(i: -1):
    while i == -1:
        i = select_item("enter item number to complete: ")
    if (todo_list[i][1]["done"] == "y"):
        print("Invalid selection!")
        return

    todo_list[i][1]["done"] = "y"

def uncomplete_item(i: -1):
    while i == -1:
        i = select_item("enter item number to uncomplete: ")

    if (todo_list[i][1]["done"] == "n"):
        print("Invalid selection!")
        return

    todo_list[i][1]["done"] = "n"

def remove_item(i : -1):
    while i == -1:
        i = select_item("enter item number to remove: ")

    todo_list.pop(i)
    for x in range(0,len(todo_list)):
        todo_list[x][1]["rank"] = x


def process_args(args):
    if len(args) > 3:
        print_usage()
    command = args[1]

    if command == "add":
        if len(args) > 2:
            add_item(args[2])
        else:
            add_item()
    elif command == "complete":
        if len(args) > 2:
            complete_item(int(args[2]))
        else:
            complete_item()
    elif command == "uncomplete":
        if len(args) > 2:
            uncomplete_item(int(args[2]))
        else:
            uncomplete_item()
    elif command == "remove":
        if len(args) > 2:
            remove_item(int(args[2]))
        else:
            remove_item()
    else:
        print_usage()
        return

    print("-"*20)
    display_list()
    write_list()



list_directory_exists = os.path.isdir(f'{home}/.pytodo')
if not list_directory_exists:
    os.mkdir(f'{home}/.pytodo')
list_exists = os.path.isfile(f'{home}/.pytodo/todo.list')
if list_exists:
    read_list()
    display_list()
else:
    print("No todo list found, creating example!")
    todo_list = example_list
    write_list()
if len(sys.argv) > 1:
    process_args(sys.argv)
    
