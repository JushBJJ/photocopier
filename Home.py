import os
import datetime
import winsound
import time

import menu
import draw
import account
import get_input


def Photocopy_Print(kwargs):
    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]
    toggle = kwargs["toggle"]

    if toggle == 0:
        action = "Photocopy"
    else:
        action = "Print"

    while True:
        screen.clear_screen()
        box = draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2),
            int(screen.get_height()/2 - box.height/2)
        )
        box.write(2, 1, action+"File: ")

        info = screen.input(screen, limit=box.width-len(action+"File: ")-2)

        if info is False:
            continue

        if user["Credits"] > 0:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ing "+info+"...") /
                      2, 1, action+"ing "+info+"...")
            time.sleep(5)

            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ed "+info+"!") /
                      2, 1, action+"ed "+info+"!")
            time.sleep(5)

            photocopier["Log"][str(datetime.datetime.now())
                               ] = action+"ed "+info
            photocopier["Ink"] -= 1
            user["Credits"] -= 1

        else:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len("Not enough credits!") /
                      2, 1, "Not enough credits!")
            time.sleep(5)

        break

    return False, [screen, photocopier, user]


def Add_Credit(kwargs):
    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]

    while True:
        screen.clear_screen()
        box = draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2),
            int(screen.get_height()/2 - box.height/2)
        )

        box.write(2, 4, "Please put an invaild number")
        box.write(2, 1, "Add credit: ")

        inpt = screen.input(screen, limit=box.width-len("Add credit File: ")-2)

        if inpt is False:
            break

        try:
            inpt = int(inpt)

            if not inpt > 0:
                continue
        except:
            continue

        user["Credits"] += inpt
        break

    screen.clear_screen()
    return False, [screen, photocopier, user]


def Settings(kwargs):
    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    users = kwargs["users"]
    username = kwargs["username"]

    screen.clear_screen()

    home_menu = menu.menu_screen(
        screen, "Home", ["Ink "+str(photocopier["Ink"]), "Settings", username])

    # Add Ink
    home_menu.add_menu("Add Ink", add_ink, False,
                       screen=screen, photocopier=photocopier, 
                       user=users[username])

    # Show Logs
    home_menu.add_menu("Show Logs", show_logs, False,
                       screen=screen, photocopier=photocopier, 
                       user=users[username])

    # Exit
    home_menu.add_menu("Exit", Exit_Photocopier, None)

    while True:
        ret, info = home_menu.select_menu()

        if ret == True:
            break
        else:
            screen = info[0]
            photocopier = info[1]
            users[username] = info[2]

            home_menu.information[0] = "Ink "+str(photocopier["Ink"])

            account.update_file(users, photocopier)

    return True, None


def show_logs(kwargs):
    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]

    for log in photocopier["Log"].keys():
        screen.write(f"{log}: "+str(photocopier["Log"][log])+"\n")

    screen.write("\nPress q to quit")
    get_input.get_key("q")

    return False, [screen, photocopier, user]


def add_ink(kwargs):
    # I insanely hate copy and pasting old code but it works fine.
    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]

    while True:
        screen.clear_screen()
        box = draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2),
            int(screen.get_height()/2 - box.height/2)
        )

        box.write(2, 1, "Add amount of ink: ")
        box.write(2, 4, "Please put an invaild number")

        inpt = screen.input(screen, limit=box.width -
                            len("Add amount of ink: ")-2)

        if inpt is False:
            break

        try:
            inpt = int(inpt)

            if not inpt > 0:
                continue
        except:
            continue

        photocopier["Ink"] += inpt
        break

    screen.clear_screen()

    return False, [screen, user, photocopier]


def Exit_Photocopier(args):
    return True, None


def home(screen, users, username, photocopier):
    screen.clear_screen()

    home_menu = menu.menu_screen(
        screen, "Home", ["Credits: "+str(users[username]["Credits"]),
                         "Home", username])

    # Photocopy
    home_menu.add_menu("Photocopy", Photocopy_Print, False,
                       screen=screen, photocopier=photocopier,
                       user=users[username], toggle=0)

    # Add Credit
    home_menu.add_menu("Add Credit", Add_Credit, False,
                       screen=screen, photocopier=photocopier,
                       user=users[username])

    # Print
    home_menu.add_menu("Print", Photocopy_Print, False,
                       screen=screen, photocopier=photocopier,
                       user=users[username], toggle=1)

    # Settings
    home_menu.add_menu("Settings", Settings, False,
                       screen=screen, photocopier=photocopier,
                       users=users, username=username)

    # Exit
    home_menu.add_menu("Exit", Exit_Photocopier, None)

    while True:
        ret, info = home_menu.select_menu()

        if ret == True:
            break
        else:
            screen = info[0]
            photocopier = info[1]
            users[username] = info[2]

            home_menu.information[0] = "Credits: " + \
                str(users[username]["Credits"])

            account.update_file(users, photocopier)

    return True, None
