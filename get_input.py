# Modified version for menu selection
import msvcrt as msv
import string

movement_keys = {
    "H": "Up",
    "P": "Down",
    "K": "Left",
    "M": "Right",

    "w": "Up",
    "s": "Down",
    "a": "Left",
    "d": "Right",

    "\r": "Return",
    "q": "quit"
}

normal_keys = string.printable
special_keys = (b"\x00", b"\xe0")


def get_single_key(k):
    while True:
        key = msv.getch()

        if key in special_keys:
            key = msv.getch().decode()
            if key == k:
                return

        else:
            key = key.decode()
            if key == k:
                return

# \x08


def get_key(screen, limit=1000):
    ret = ""

    while True:
        key = msv.getch()

        if key in special_keys:
            msv.getch()

        elif key.decode() == "\r":
            return ret

        elif key.decode() in normal_keys:
            if limit > 0:
                key = key.decode()
                ret += key
                screen.write(key)
                limit -= 1

        elif key.decode() == "\x08":
            return False  # Backspace


def input_movement():
    while True:
        key = msv.getch()

        if key in special_keys:
            key = msv.getch().decode()

            if key in movement_keys.keys():
                return movement_keys[key]
        else:
            key = key.decode()
            if key in normal_keys:
                if key in movement_keys.keys():
                    return movement_keys[key]
