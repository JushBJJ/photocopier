import menu
import draw
import time
import os
import datetime

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

        info=screen.input(screen, limit=box.width-len(action+"File: ")-2)
        
        if info=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif info=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break

        if credits["Credits"]>0:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ing "+info+"...")/2, 1, action+"ing "+info+"...")
            time.sleep(5)

            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len(action+"ed "+info+"!")/2, 1, action+"ed "+info+"!")
            time.sleep(5)

            photocopier["Log"][str(datetime.datetime.now())]=action+"ed "+info
            photocopier["Ink"]-=1
            credits["Credits"]-=1
        
        else:
            box.write(2, 1, " "*box.width)
            box.write(box.width/2-len("Not enough credits!")/2, 1, "Not enough credits!")
            time.sleep(5)

        break

def Add_Credit(info):
    screen=info[0]
    photocopier=info[1]
    credits=info[2]

    while True:
        screen.clear_screen()
        box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2), 
            int(screen.get_height()/2 - box.height/2)
        )

        box.write(2, 4, "Please put an invaild number")
        box.write(2, 1, "Add credit: ")

        info=screen.input(screen, limit=box.width-len("Add credit File: ")-2)
        
        if info=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif info=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break
        
        try:
            info=int(info)
        except:
            continue

        credits["Credits"]+=info
        break

def Settings(info):
    screen=info[0]
    photocopier=info[1]
    user=info[2]
    username=info[3]

    while True:
        screen.clear_screen()
        
        settings=menu.menu_screen(screen, "Settings", ["Credits"+str(user["credits"]), "Settings", username])
        settings.add_menu("Add Ink", add_ink, [screen, photocopier])
        settings.add_menu("Exit", Exit_Photocopier, None)

        settings.select_menu()

def add_ink(info):
    # I insanely hate copy and pasting old code but it works fine.
    screen=info[0]
    photocopier=info[1]

    while True:
        screen.clear_screen()
        box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)

        box.draw(
            int(screen.get_width()/2 - box.width/2), 
            int(screen.get_height()/2 - box.height/2)
        )
        box.write(2, 1, "Add amount of ink: ")

        info=screen.input(screen, limit=box.width-len("Add amount of ink: ")-2)
        
        if info=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b":
            continue
        elif info=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf":
            break
        
        try:
            info=int(info)
        except:
            box.write(2, 4, "Please put an invaild number")
            continue

        photocopier["Ink"]+=info
    

def Exit_Photocopier():
    return "EXIT"

def home(screen, users, username, photocopier):
    screen.clear_screen()

    user=users[username]
    home_menu=menu.menu_screen(screen, "Home", ["Credits: "+str(user["Credits"]), "Home", username])
    home_menu.add_menu("Photocopy", Photocopy_Print, [screen, photocopier, user, "Photocopy"])
    home_menu.add_menu("Add Credit", Add_Credit, [screen, photocopier, user])
    home_menu.add_menu("Print", Photocopy_Print, [screen, photocopier, user, "Print"])
    home_menu.add_menu("Settings", Settings, [screen, photocopier, user, username])
    home_menu.add_menu("Exit", Exit_Photocopier, None)

    home_menu.select_menu()