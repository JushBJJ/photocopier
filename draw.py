""" Draw functions for photocopier, though this is very specific
and only rectangles are going to be used. """

# Rectangles in this case are automatically unfilled.


class rectangle:
    """ Rectangle class for drawing boxes for the photocopier """

    def __init__(self, scr, width, height):
        self.screen = scr

        self.width = width
        self.height = height
        self.location = []

    def draw(self, x, y, key="#"):
        """ Draw function using whatever key is specifed """

        self.location = [x, y]

        # Draw rectangle.
        for line in range(y, y+self.height+1):
            self.screen.cursor.to_pos(x, line)

            if line in (y, y+self.height):
                self.screen.pre_write(key*(self.width+1))

            else:
                self.screen.pre_write(key)
                self.screen.cursor.to_pos(x+self.width, line)
                self.screen.pre_write(key)

        self.screen.flush()

    def write(self, x, y, string):
        """ Write function to put strings into boxes.

            Dimensions of a rectange (example)
              01234567
            0 --------
            1 -      -
            2 -      -
            3 --------
        """

        x += self.location[0]
        y += self.location[1]

        self.screen.cursor.to_pos(x, y)

        # Write string in position
        for letter in string:
            if x == self.location[0]+self.width:
                break

            self.screen.pre_write(letter)
            x += 1

        self.screen.flush()

    def to_pos(self, x, y):
        """ Move cursor relative to the box dimensions """

        self.screen.cursor.to_pos(x+self.location[0], y+self.location[1])
