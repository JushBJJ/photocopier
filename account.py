""" Account management """

import json
import hashlib
import os
from typing import Dict
import draw


user: Dict[None, None] = {}
photocopier: Dict[None, None] = {}

# File location.
file_Path = os.path.join(os.environ["HOMEPATH"], "Desktop\\Accounts.json")
photocopier_Path = os.path.join(
    os.environ["HOMEPATH"], "Desktop\\Photocopier.json")


def update_file(users, _photocopier):
    fix_file()

    with open(file_Path, "w") as f:
        f.write(json.dumps(users))

    with open(photocopier_Path, "w") as f:
        f.write(json.dumps(_photocopier))

def fix_file():
    _accounts = None
    _photocopier = None

    try:
        with open(file_Path, "r") as users_File:
            _accounts = json.loads(users_File.read())

        with open(photocopier_Path, "r") as photocopier_File:
            _photocopier = json.loads(photocopier_File.read())

    finally:
        _photocopier = {"Ink": 100,
                        "Log":{}
                        }

        _accounts = {"Admin":
                     {"Password": hashlib.sha256("admin".encode()).hexdigest(),
                      "Credits": 1000
                      }
                     }

        with open(file_Path, "w") as users_File:
            users_File.write(json.dumps(_accounts))

        with open(photocopier_Path, "w") as photocopier_File:
            photocopier_File.write(json.dumps(_photocopier))

    return _accounts, _photocopier


def rect_middle(height, scr):
    """ For drawing rectangles in the middle """

    width = int(scr.get_width()/2)

    rectangle_x = int(scr.get_width()/2 - width/2)
    rectangle_y = int(scr.get_height()/2)

    rect = draw.rectangle(scr, width, height)

    return rect, rectangle_x, rectangle_y


def rect_write_title(rect, string, bottom=False):
    """ For writing titles at the top of the ui box """

    width = rect.width/2
    title_x = width - len(string)/2
    title_y = -2 if not bottom else rect.height + 2

    rect.write(title_x, title_y, string)


def register_or_login(kwargs):
    """ If register is false, login is switched on """
    # Using CSV for this is just for testing, not for real security purposes.
    # Update: Relationship with CSV ended, json is now my new friend...again

    screen = kwargs["screen"]
    toggle = kwargs["toggle"]
    height = 4

    failed_login = ["Invaild username or password, try again.",
                    "Username already exists"]
    title = "Login" if toggle else "Register"

    _users, _photocopier = fix_file()

    ui_box, ui_x, ui_y = rect_middle(height, screen)
    ui_box.draw(ui_x, ui_y)

    space_length = len("Username: ")+1*ui_box.width-1

    # Write username and password
    while True:
        ui_box.write(2, 1, "Username: "+" "*space_length)
        ui_box.write(2, 2, "#" * (ui_box.width-2))
        ui_box.write(2, 3, "Password: ")

        rect_write_title(ui_box, title)

        # Input
        mode, username, password = ask_info(screen, ui_box,
                                            _users, _photocopier, toggle)

        if mode == 3:
            _users[username] = {}
            _users[username]["Password"] = password
            _users[username]["Credits"] = 100

            update_file(_users, _photocopier)

        elif mode in (0, 1):
            rect_write_title(ui_box, failed_login[mode], bottom=True)
            continue

        break

    return False, [screen, _users, username, _photocopier]


def ask_info(screen, ui_box, _users, _photocopier, toggle):
    """ For asking the user for username and password,

        Mode 0 -> Failed Login
        Mode 1 -> Failed Register
        Mode 2 -> Successful Login
        Mode 3 -> Successful Register

    """

    while True:
        input_limit = 2+len("Username: ")*ui_box.width-1

        # Clear
        ui_box.write(1+len("Username: "), 1, " "*input_limit)
        ui_box.write(1+len("Password: "), 3, " "*input_limit)

        ui_box.to_pos(1+len("Username: "), 1)
        username = screen.input(screen, limit=input_limit)

        # When user presses Backspace
        if username is False:
            continue

        # Otherwise...
        ui_box.to_pos(1+len("Password: "), 3)
        password = screen.input(screen, limit=input_limit)

        if password is False:
            continue

        # Hash it
        password = str(hashlib.sha256(password.encode()).hexdigest())

        # Checking
        if toggle:
            if username in _users:
                if _users[username]["Password"] == password:
                    # Login
                    return 2, username, None  # Successful Login

            return 0, None, None  # Failed login

        # Register
        if username in _users:
            return 1, None, None  # Failed register

        return 3, username, str(password)  # Sucessful Register
