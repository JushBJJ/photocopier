import os
import datetime
import winsound
import time

import menu
import draw
import account
import get_input

# rect_middle(height, scr): rect_write_title(rect, string, bottom=False)


def Photocopy_Print(kwargs):
    """ Photocopying or printing """

    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]
    toggle = kwargs["toggle"]

    if toggle == 0:
        title = "Photocopy"
        process = "Photocopying..."
        processed = "Photocopied!"

    else:
        title = "Print"
        process = "Printing..."
        processed = "Printed!"

    # Create box
    box, x, y = account.rect_middle(2, screen)
    box.draw(x, y)
    account.rect_write_title(box, title)

    while True:
        box.write(1, 1, "File: "+" "*(box.width-1))
        box.to_pos(1+len("File: "), 1)

        # User input
        file_name = screen.input(screen, limit=box.width-len("File: ")+1)

        if file_name is False:
            continue

        # Log and process photocopying or printing file
        photocopier[str(datetime.datetime.now())] = title + " " + file_name

        box.write(1, 1, " "*(box.width-1))
        box.write(box.width/2-len(process)/2, 1, process)

        time.sleep(3)

        box.write(1, 1, " "*(box.width-1))
        box.write(box.width/2-len(processed)/2, 1, processed)

        time.sleep(3)
        break

    return False, [screen, photocopier, user]


def Add_Credit(kwargs):
    """ lol i copied and pasted the code from the photcopier_print function
    cause it just works """

    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]

    title = "Add credit"

    # Create box
    box, x, y = account.rect_middle(2, screen)
    box.draw(x, y)
    account.rect_write_title(box, title)

    while True:
        box.write(1, 1, "Amount: "+" "*(box.width-1))
        box.to_pos(1+len("Amount: "), 1)

        # User input
        credit = screen.input(screen, limit=box.width-len("Amount: ")+1)

        if credit is False:
            continue
       
        if not credit.isdigit():
            box.write(int(box.width/len("Put an invaild number!")/2), 3, "Put an invaild number!")
        else:
            credit = int(credit)
            user["Credits"] += credit

            # Log and process photocopying or printing file
            photocopier[str(datetime.datetime.now())] = title + str(credit)
            break
        continue

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

        if ret:
            account.update_file(users, photocopier)
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
    """ lol i copied and pasted the code from the photcopier_print function
    cause it just works """

    screen = kwargs["screen"]
    photocopier = kwargs["photocopier"]
    user = kwargs["user"]

    title = "Add Ink"

    # Create box
    box, x, y = account.rect_middle(2, screen)
    box.draw(x, y)
    account.rect_write_title(box, title)

    while True:
        box.write(1, 1, "Amount: "+" "*(box.width-1))
        box.to_pos(1+len("Amount: "), 1)

        # User input
        ink = screen.input(screen, limit=box.width-len("Amount: ")+1)

        if ink is False:
            continue
       
        if not ink.isdigit():
            box.write(int(box.width/len("Put an invaild number!")/2), 3, "Put an invaild number!")
        else:
            ink = int(ink)
            photocopier["Ink"] += ink

            # Log and process photocopying or printing file
            photocopier[str(datetime.datetime.now())] = title + str(ink)
            break
        continue

    screen.clear_screen()
    return False, [screen, photocopier, user]


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
    home_menu.add_menu("Exit", Exit_Photocopier, False, yes="yes")

    while True:
        ret, info = home_menu.select_menu()

        if ret:
            account.update_file(users, photocopier)
            break
        else:
            screen = info[0]
            photocopier = info[1]
            users[username] = info[2]

            home_menu.information[0] = "Credits: " + \
                str(users[username]["Credits"])

            account.update_file(users, photocopier)

    return False, None
