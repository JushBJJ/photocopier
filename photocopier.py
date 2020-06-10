import os
import time
import screen
import account
import menu
import draw
import Home


def shutdown(args):
    scr = args["screen"]  # Screen

    # Not actually shutting down computer or anything..
    box = draw.rectangle(scr, int(os.get_terminal_size()[0]/2), 2)
    box.draw(int(scr.get_width()/2 - box.width/2),
             int(scr.get_height()/2 - box.height/2))
    box.write(box.width/2-len("Shutting down...")/2, 1, "Shutting down...")

    time.sleep(5)
    return True, None


def main():
    """ Main function for photocopier, this is where it starts. """

    # Toggle: 1 -> Register
    # Toggle: 0 -> Login

    scr = screen.Screen()
    menu1 = menu.menu_screen(
        scr, "Start", ["", "Welcome to the Boring Company photocopier", ""])

    # Login
    menu1.add_menu("Login", account.register_or_login, False, screen=scr,
                   toggle=True)

    # Register
    menu1.add_menu("Register", account.register_or_login, False, screen=scr,
                   toggle=False)

    # Shutdown
    menu1.add_menu("Shutdown", shutdown, False, screen=scr)

    menu1.print_menu()
    ret, info = menu1.select_menu()

    if not ret:
        account.fix_file()
        Home.home(info[0], info[1], info[2], info[3])

    else:
        return


if __name__ == "__main__":
    main()
