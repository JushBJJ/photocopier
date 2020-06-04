import screen
import account
import menu
import draw
import os
import time

def shutdown(args):
    screen=args[0]

    # Not actually shutting down computer or anything..
    box=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 2)
    box.draw(int(screen.get_width()/2 - box.width/2), int(screen.get_height()/2 - box.height/2))
    box.write(box.width/2-len("Shutting down...")/2, 1, "Shutting down...")

    time.sleep(5)

def main():
    scr=screen.Screen()
    menu1=menu.menu_screen(scr, "Start", ["", "Welcome to the Boring Company photocopier",""])
    menu1.add_menu("Login", account.register_or_login, [scr, 0], newline=True)
    menu1.add_menu("Register", account.register_or_login, [scr, 1], newline=True)
    menu1.add_menu("Shutdown", shutdown, [scr], newline=True)

    menu1.print_menu()
    menu1.select_menu()

if __name__ == "__main__":
    main()