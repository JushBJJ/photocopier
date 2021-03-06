""" Menu functions used to create interactive menus in
the photocopier """


# Headers are a dict that splits it's statuses from
# the top of the screen according to screen size width


class menu_screen:
    """ Class for menu screens, interactable and (slightly) customizeable """

    def __init__(self, scr, name, information):
        """ Format of self.information is:
              1. Title (Automatically Centered)

              2. Left self.information (Automatically put in the left
                 of the screen

              3. Right self.information (Automatically put in the right
                 of the screen, cursor is positioned
                 (maximum_length - string_length)

             All are required, but can just be filled with nothing. """

        self.menus = {}
        self.lines = {}

        self.name = name
        self.screen = scr

        self.information = information

    def add_menu(self, name, function_address, newline, **kwargs):
        """ Adds a menu for menu selecting """

        if len(self.menus.keys()) == 0:
            self.menus[name] = {}
            self.menus[name]["address"] = function_address
            self.menus[name]["new_line"] = newline

            self.menus[name]["x"] = 1
            self.menus[name]["y"] = 3

            self.menus[name]["selected"] = True

        else:
            last_pos = self.update_menu_positions()

            self.menus[name] = {}
            self.menus[name]["address"] = function_address
            self.menus[name]["new_line"] = newline

            self.menus[name]["x"] = (
                last_pos[0]+8 if not self.menus[name]["new_line"] else 1)
            self.menus[name]["y"] = last_pos[1] + \
                (1 if self.menus[name]["new_line"] else 0)

            self.menus[name]["selected"] = False

            self.update_menu_positions()

        # When the cursor moves up or down, it needs to stay at the same place
        # but y is changed.

        line = self.menus[name]["y"]
        self.menus[name]["args"] = kwargs  # Arguments of the function

        if line not in self.lines:
            self.lines[line] = {}
        self.lines[line][len(self.lines[line])] = self.menus[name]

    # Delete_menu function isn't needed for this photocopying

    def update_menu_positions(self):
        """ Goes through the existing menus and
        re-positions them correctively. """

        start = True
        last_pos = [0, 0]

        screen_width = self.screen.get_width()

        for menu in self.menus:
            if start:
                self.menus[menu]["x"] = 1
                # Because the information is 3 lines long
                self.menus[menu]["y"] = 3
                start = False

            if self.menus[menu]["x"]+len(menu) >= screen_width:
                # Magically put the menu to the next line
                self.menus[menu]["x"] = 1
                self.menus[menu]["y"] += 1

            if self.menus[menu]["x"] == last_pos[0] and\
                    self.menus[menu]["y"] == last_pos[1]:
                # Move menu by 8 spaces apart.

                self.menus[menu]["x"] = last_pos[0]+8
                self.menus[menu]["y"] = last_pos[1]

            # FIX when screen height is too low here

            last_pos[0] = self.menus[menu]["x"]+len(menu)
            last_pos[1] = self.menus[menu]["y"]

        return last_pos

    def debug_write(self, string):
        """ For debug purposes """

        self.screen.cursor.load_position("Debug")
        self.screen.cursor.to_pos(
            self.screen.get_width()/2-len(string)/2, self.screen.cursor.y)

        self.screen.clear_line()
        self.screen.write(string)

    def select_menu(self):
        """ Function for selecting menus and interacting with them """

        last_y = 3
        last_id = 0
        # First menu is automatically in line 3, id 0
        last_menu = self.lines[last_y][last_id]

        while True:
            # Reset the default selected menu
            for line in self.lines:
                for line_id in self.lines[line]:
                    self.lines[line][line_id]["selected"] = False

            last_menu["selected"] = True

            self.print_menu()
            self.debug_write(
                f"Press WASD or arrow keys to move. " +
                "Press Enter to select a menu. Press q to exit")

            # Pre-define the next movements on whatever the user presses.
            pre_move = {
                "Up": (last_y-1, last_id),
                "Down": (last_y+1, last_id),
                "Left": (last_y, last_id-1),
                "Right": (last_y, last_id+1),

                "Return": (0, 3)
            }

            key = self.screen.input_movement()

            # last_menu shares the same memory address as the original defined
            # in add_menu function

            # magical memories!
            if key == "Return":
                self.screen.clear_screen()
                ret, info = last_menu["address"](last_menu["args"])
                self.screen.clear_screen()

                if not ret:
                    return ret, info
                else:
                    return True, None

            elif key == "quit":
                self.screen.clear_screen()
                return True, None

            else:
                # This is to stop the user from selecting
                # non-existant menu thingys

                y = pre_move[key][0]
                x = pre_move[key][1]

                if y not in self.lines or x not in self.lines[y]:
                    continue

            last_y, last_id = pre_move[key]

            # Manage whoever needs to get hightlighted when printed
            if last_y in self.lines:
                if last_id in self.lines[last_y]:
                    last_menu["selected"] = False

                    last_menu = self.lines[last_y][last_id]
                    last_menu["selected"] = True

    def print_menu(self):
        """ self.screen is used so it goes to the same addresses.

            Format for menus is (Dictionary Format):
             {"Menu Name Example": function_address,
             ...
             }"""

        if self.screen.width != self.screen.get_width() or \
                self.screen.height != self.screen.get_height():

            self.screen.width = self.screen.get_width()
            self.screen.height = self.screen.get_height()

            self.screen.clear_screen()

        self.update_menu_positions()
        max_x = self.screen.get_width()

        # Print Menu self.information
        # To minimise amount of typing needed

        left = self.information[0]
        center = self.information[1]
        right = self.information[2]

        # Left information
        self.screen.cursor.to_pos(1, 1)
        self.screen.pre_write(left)

        # Title
        self.screen.cursor.to_pos(max_x/2-len(center)/2, 1)
        self.screen.pre_write(center)

        # Right information
        self.screen.cursor.to_pos(max_x-len(self.information[0])/2-1, 1)
        self.screen.pre_write(right)

        self.screen.pre_write("\n"+"_"*max_x+"\n")
        self.screen.flush()

        # Print menus
        for menu_titles in self.menus:
            if self.menus[menu_titles]["selected"]:
                self.screen.background_colour("WHITE", flush=False)
                self.screen.foreground_colour("BLACK", flush=False)

            x = self.menus[menu_titles]["x"]
            y = self.menus[menu_titles]["y"]

            self.screen.cursor.to_pos(x, y)
            self.screen.pre_write(menu_titles)

            # Messy, just messy

            self.screen.background_colour("RESET")
            self.screen.foreground_colour("RESET")

            self.screen.pre_write("\n")
            self.screen.flush()
