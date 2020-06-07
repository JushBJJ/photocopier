import screen
import os

# Rectangles in this case are automatically unfilled.
class rectangle:
    def __init__(self, screen, width, height):
        self.screen=screen

        self.width=width
        self.height=height
        self.location=[]

    def draw(self, x, y, key="#"):
        self.location=[x,y]

        # Draw rectangle.
        for line in range(y, y+self.height+1):
            self.screen.local_cursor.to_pos(x, line)

            if line==y or line==y+self.height:
                self.screen.pre_write(key*(self.width+1))

            else:
                self.screen.pre_write(key)
                self.screen.local_cursor.to_pos(x+self.width, line)
                self.screen.pre_write(key)
        
        self.screen.flush()
    
    def write(self, x, y, string):
        """
            Dimensions of a rectange (example)
              01234567 
            0 -------- 
            1 -      -
            2 -      -
            3 --------
        """
        
        x+=self.location[0]
        y+=self.location[1]

        self.screen.local_cursor.to_pos(x,y)

        # Write string in position
        for letter in string:
            if x==self.location[0]+self.width: 
                break

            self.screen.pre_write(letter)
            x+=1

        self.screen.flush()
    
    def to_pos(self, x, y):
        self.screen.local_cursor.to_pos(x+self.location[0], y+self.location[1])

"""scr=screen.Screen()
rect=rectangle(scr, int(os.get_terminal_size()[0]/2), 4)
rect.draw(int((os.get_terminal_size()[0]/2))-int(rect.width/2), int((os.get_terminal_size()[1]/2))-int(rect.height/2)) # Draw box at middle of screen.
rect.write(2, 1, "Username: ")
rect.write(1, 2, "-"*rect.width)
rect.write(2, 3, "Password: ")"""
