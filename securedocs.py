# 3

# Modules Imported
import csv
import os
from getpass import getpass
import json
import random

# Determines Current User
user = ""

# Opens users.csv
with open("users.csv", "r") as f:
    t = csv.reader(f)
    global_users = dict(t).copy()
# Opens decode.json
with open("decode.json", "r") as f:
    k = json.load(f)

# Encryption
def encrypt(para, fac):
    a = ""
    for i in para:
        a += chr(ord(i) + fac)
    return a


# Decryption
def decrypt(para, fac):
    a = ""
    for i in para:
        a += chr(ord(i) - fac)
    return a


# Register
def register():
    global user
    global k
    username = input("Enter a username : ")
    while username in global_users:
        print("Username already Exists. Please enter another username.")
        username = input("Enter a username : ")
    password = getpass("Enter your password : ")
    conf_password = getpass("Confirm your password : ")
    while password != conf_password:
        print("Passwords Don't match Please enter again!")
        password = getpass("Enter your password : ")
        conf_password = getpass("Confirm your password : ")
    global_users.update({username: password})
    user = username
    with open("users.csv", "a", newline="\n") as f2:
        w = csv.writer(f2)
        w.writerow([username, password])
    k.update({username: random.randint(1, 15)})
    fp = open("decode.json", "w")
    json.dump(k, fp)
    fp.close()
    print("User Created Succesfully!")


def startlogin():
    global user
    global k
    username = input("Enter your username : ")
    password = getpass("Enter your password: ")
    if username in global_users:
        while global_users[username] != password:
            print("Invalid Password! Please enter again!")
            password = getpass("Enter your password: ")
        if global_users[username] == password:
            print("Logged in successfully!")
            user = username
    else:
        print("User doesn't exist")


def start():
    global user
    while user == "":
        print("Are you new here?")
        u_inp = input("Y/N : ")
        while u_inp not in ["Y", "N"]:
            os.system("cls")
            print("Are you new here?")
            u_inp = input("Y/N : ")
        match u_inp:
            case "N":
                print("Great! Please enter your login details")
                startlogin()
            case "Y":
                print("Hello newface! Please enter a username and password")
                register()
            case _:
                print("Invalid Input!")


def newnote(name):
    global user
    os.system("cls")
    with open(f".\\{user}Notes\\{user}_{name}.txt", "a+") as f:
        para = ""
        print(f"Writing to {user}_{name}.txt...\n")
        print("Enter your content of note here : \n\n")
        with open("decode.json", "r") as fpjson:
            k = json.load(fpjson)
        fac = k[user]
        u = input()
        while len(u) != 0:
            para += encrypt(u, fac) + "\n"
            u = input()
        f.write(para)


def readexisting():
    global user
    global k
    os.system("cls")
    dirs = os.listdir(f".\\{user}Notes")
    dirs_sel = []
    print("Available Notes to read : ")
    for ind, value in enumerate(dirs, start=1):
        dirs_sel.append([ind, value])
        value = value.lstrip(f"{user}_")
        value = value.rstrip(".txt")
        print(f"{ind}. {value}")

    try:
        user_inp = int(input("Enter the serial number of file you want to read : "))
    except:
        user_inp = 0

    while user_inp not in range(1, len(dirs) + 1):
        if user_inp == -1:
            break
        os.system("cls")
        print("Available Notes to read : ")
        for ind, value in enumerate(dirs, start=1):
            dirs_sel.append([ind, value])
            value = value.lstrip(f"{user}_")
            value = value.rstrip(".txt")
            print(f"{ind}. {value}")
        try:
            user_inp = int(input("Enter the serial number of file you want to read : "))
        except:
            user_inp = 0
    print("\n\n")
    os.system("cls")
    if user_inp != -1:
        print(f"Currently reading -> {dirs_sel[user_inp-1][1]}")
        with open("decode.json", "r") as jsonread:
            usrs = json.load(jsonread)
        fac = usrs[user]
        with open(f".\\{user}Notes\\{dirs_sel[user_inp-1][1]}", "r") as f:
            t = f.readlines()
            for i in t:
                i = i.rstrip("\n")
                i = decrypt(i, fac)
                print(i)
        print("\n\n")
        user_inp = input("Press Enter to return...")


def deleteexisting():
    global user
    global k
    os.system("cls")
    dirs = os.listdir(f".\\{user}Notes")
    dirs_sel = []
    print("Available Notes to delete : ")
    for ind, value in enumerate(dirs, start=1):
        dirs_sel.append([ind, value])
        value = value.lstrip(f"{user}_")
        value = value.rstrip(".txt")
        print(f"{ind}. {value}")

    try:
        user_inp = int(input("Enter the serial number of file you want to delete : "))
    except:
        user_inp = 0

    while user_inp not in range(1, len(dirs) + 1):
        os.system("cls")
        if user_inp == -1:
            break
        print("Available Notes to delete : ")
        for ind, value in enumerate(dirs, start=1):
            dirs_sel.append([ind, value])
            value = value.lstrip(f"{user}_")
            value = value.rstrip(".txt")
            print(f"{ind}. {value}")
        try:
            user_inp = int(
                input("Enter the serial number of file you want to delete : ")
            )
        except:
            user_inp = 0

    if user_inp != -1:
        os.remove(f".\\{user}Notes\\{dirs_sel[user_inp-1][1]}")
        print("Note deleted successfully!")
        input("Press Enter to return...")


def main():
    global user
    os.system("cls")
    print("Welcome to SecureNotes 📝")
    print("A perfect place to manage your notes and important info!")
    start()
    os.system("cls")
    try:
        os.mkdir(f"{user}Notes")
    except:
        pass
    while True:
        os.system("cls")
        print(f"Howdy! {user}!")
        print("What would you like to do today?")
        print(
            "1. Write new note\n2. Read existing Notes\n3. Delete Existing files\n4. Logout"
        )
        print("(Enter -1 anywhere to go back to the previous panel)")
        u_i = input("Enter your choice : ")
        while u_i not in ["1", "2", "3", "4"]:
            os.system("cls")
            print("Invalid Choice! Please enter again!")
            print(
                "1. Write new note\n2. Read existing Notes\n3. Delete Existing files\n4. Logout"
            )
            u_i = input("Enter your choice : ")
        match u_i:
            case "1":
                os.system("cls")
                name = input("Write a name to your note : ")
                newnote(name)
            case "2":
                readexisting()
            case "3":
                deleteexisting()
            case "4":
                os.system("cls")
                print("Logged out successfully! Thanks for using SecureNotes!")
                curr_user = ""
                break


main()
