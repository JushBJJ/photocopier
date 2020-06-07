import menu
import draw
import time
import os
import datetime
import account
import get_input

def Photocopy_Print(info):
    screen=info[0]
    photocopier=info[1]
    credits=info[2]
    action=info[3]

    while True:
        screen.clear_screen()
        box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2), 
            int(screen.get_height()/2 - box.height/2)
        )
        box.write(2, 1, action+"File: ")

        inpt=screen.input(screen, limit=box.width-len(action+"File: ")-2)
        
        if inpt=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif inpt=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break

        if credits["Credits"]>0:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ing "+inpt+"...")/2, 1, action+"ing "+inpt+"...")
            time.sleep(5)

            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ed "+inpt+"!")/2, 1, action+"ed "+inpt+"!")
            time.sleep(5)

            photocopier["Log"][str(datetime.datetime.now())]=action+"ed "+inpt
            photocopier["Ink"]-=1
            credits["Credits"]-=1
        
        else:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len("Not enough credits!")/2, 1, "Not enough credits!")
            time.sleep(5)

        break

    screen.clear_screen()
    return False, (info[0], info[1], info[2])

def Add_Credit(info):
    screen=info[0]
    photocopier=info[1]
    user=info[2]

    while True:
        screen.clear_screen()
        box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2), 
            int(screen.get_height()/2 - box.height/2)
        )

        box.write(2, 4, "Please put an invaild number")
        box.write(2, 1, "Add credit: ")

        inpt=screen.input(screen, limit=box.width-len("Add credit File: ")-2)
        
        if inpt=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif inpt=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break
        
        try:
            inpt=int(inpt)
        except:
            continue

        user["Credits"]+=inpt
        break

    screen.clear_screen()
    return False, (info[0], info[1], info[2])

def Settings(info):
    screen=info[0]
    photocopier=info[1]
    users=info[2]
    username=info[3]

    screen.clear_screen()

    home_menu=menu.menu_screen(screen, "Home", ["Ink "+str(photocopier["Ink"]), "Settings", username])
    home_menu.add_menu("Add Ink", add_ink, [screen, photocopier, users[username]])
    home_menu.add_menu("Show Logs", show_logs, [screen, photocopier, users[username]])
    home_menu.add_menu("Exit", Exit_Photocopier, None)

    while True:
        ret, info=home_menu.select_menu()

        if ret==True:
            break
        else:
            screen=info[0]
            photocopier=info[1]
            users[username]=info[2]

            home_menu.information[0]="Ink "+str(photocopier["Ink"])

            account.update_file(users, photocopier)

    return True, None

def show_logs(info):
    screen=info[0]
    photocopier=info[1]
    user=info[2]

    for log in photocopier["Log"].keys():
        screen.write(f"{log}: "+str(photocopier["Log"][log])+"\n")

    screen.write("\nPress q to quit")
    get_input.get_key("q")

    return False, (info[0], info[1], info[2])

def add_ink(info):
    # I insanely hate copy and pasting old code but it works fine.
    screen=info[0]
    photocopier=info[1]
    user=info[2]

    while True:
        screen.clear_screen()
        box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2), 
            int(screen.get_height()/2 - box.height/2)
        )

        box.write(2, 1, "Add amount of ink: ")
        box.write(2, 4, "Please put an invaild number")

        inpt=screen.input(screen, limit=box.width-len("Add amount of ink: ")-2)
        
        if inpt=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif inpt=="8e35c2cd3e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break
        
        try:
            inpt=int(inpt)
        except:
            continue

        photocopier["Ink"]+=inpt
        break
    
    screen.clear_screen()

    return False, (info[0], info[1], info[2])

def Exit_Photocopier(info):
    return True, None

def home(screen, users, username, photocopier):
    screen.clear_screen()

    home_menu=menu.menu_screen(screen, "Home", ["Credits: "+str(users[username]["Credits"]), "Home", username])
    home_menu.add_menu("Photocopy", Photocopy_Print, [screen, photocopier, users[username], "Photocopy"])
    home_menu.add_menu("Add Credit", Add_Credit, [screen, photocopier, users[username]])
    home_menu.add_menu("Print", Photocopy_Print, [screen, photocopier, users[username], "Print"])
    home_menu.add_menu("Settings", Settings, [screen, photocopier, users, username])
    home_menu.add_menu("Exit", Exit_Photocopier, None)

    while True:
        ret, info=home_menu.select_menu()

        if ret==True:
            break
        else:
            screen=info[0]
            photocopier=info[1]
            users[username]=info[2]

            home_menu.information[0]="Credits: "+str(users[username]["Credits"])

            account.update_file(users, photocopier)

    return True, None