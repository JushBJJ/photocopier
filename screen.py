import colorama
import get_input
import sys
import os

class Screen_Cursor:
	"""
		Screen_Cursor class is just to make my life easier by positioning the cursor within menus and other 
		stuff needed.

		It automatically defaults the x and y for certain reasons that break the command prompt.
		It has input function that finds simply returns the arrow or wasd keys that will be used to position the cursor.
		to_pos is used to position the cursor.
	"""
	def __init__(self, Screen):
		# Automatically sets the cursor position to x:1, y:1
		self.screen=Screen

		self.x, self.y=1,1
		self.saved_positions={}

	def save_position(self, name, position):
		# Saves the positions, used for menu selection
		# Position type must be a list containing [x,y]
		self.saved_positions[name]={}
		self.saved_positions[name]["x"]=position[0]
		self.saved_positions[name]["y"]=position[1]

	def load_position(self, name):
		# Moves the cursor to the cursor position
		x=self.saved_positions[name]["x"]
		y=self.saved_positions[name]["y"]

		self.to_pos(x,y)

	def input(self):
		# Get arrow key and WASD key input
		return get_input.input_movement()

	def to_pos(self, x,y):
		# Moves the cursor to the given position.

		if type(x) is float:
			x=int(x)
			
		self.screen.write(colorama.Cursor.POS(x,y), ansi=True)
		self.x=x
		self.y=y

		return x,y

	def reset_pos(self):
		# Resets the cursor position to 1,1
		return self.to_pos(1,1)

	def pos_up(self, y=1):
		# Moves the cursor up by y
		self.y-=y
		return self.to_pos(self.x, self.y)

	def pos_down(self, y=1):
		# Moves the cursor down by y
		self.y+=y
		return self.to_pos(self.x, self.y)

class Screen:
	"""
		Screen class basically initialises the screen which will modify stdout
		Includes clear_line, clear_screen, manual flushing and getting the 
		screen amount of columns and lines
	"""
	def __init__(self):
		# Automatically initialises the terminal and cursor.
		colorama.init(wrap=True) # Wraps stdout to enable most ansi support
		self.stdout=sys.stdout
		self.local_cursor=Screen_Cursor(self)
		self.local_cursor.to_pos(self.get_width()-1, self.get_height()-1)

		self.width=self.get_width()
		self.height=self.get_height()

		self.clear_screen()

		# foreground_colours and background_colours is pretty much copy and pasted from colourama's ansi source 
		# but put into a dictionary just so things are easier when printing out forground colours
		self.foreground_colours={
			"BLACK"           : "\x1b[30m",
			"RED"             : "\x1b[31m",
			"GREEN"           : "\x1b[32m",
			"YELLOW"          : "\x1b[33m",
			"BLUE"            : "\x1b[34m",
			"MAGENTA"         : "\x1b[35m",
			"CYAN"            : "\x1b[36m",
			"WHITE"           : "\x1b[37m",
			"RESET"           : "\x1b[39m"
		}

		self.background_colours={
			"BLACK"           : "\x1b[40m",
			"RED"             : "\x1b[41m",
			"GREEN"           : "\x1b[42m",
			"YELLOW"          : "\x1b[43m",
			"BLUE"            : "\x1b[44m",
			"MAGENTA"         : "\x1b[45m",
			"CYAN"            : "\x1b[46m",
			"WHITE"           : "\x1b[47m",
			"RESET"           : "\x1b[49m"
		}

	def foreground_colour(self, colour, flush=True):
		# Change foreground colour (text colour)
		self.pre_write(self.foreground_colours[colour])

		if flush: self.flush()

	def background_colour(self, colour, flush=True):
		# Change background colour
		self.pre_write(self.background_colours[colour])

		if flush: self.flush()

	def getkey(self, key):
		# Waits until user has pressed the key given
		return get_input.get_single_key(key)
	
	def input_movement(self):
		return self.local_cursor.input()

	def flush(self):
		# Flushes stdout
		self.stdout.flush()

	def auto_position(self, string):
		# This automatcally updates the position variables of the cursor.
		# Can possibly lead to peformance issues within writing to stdout
		for i in range(len(string)):
			if string[i]=="\n":
				self.local_cursor.x=1
				self.local_cursor.y+=1
			else:
				self.local_cursor.x+=i

	def write(self, string, ansi=False):
		# Manually writes stdout and automatically updates cursor position
		# If ansi is true, it doesn't update the cursor position.
		self.stdout.write(string)
		self.stdout.flush()	

		if not ansi: 
			self.auto_position(string)

	def pre_write(self, string, ansi=False):
		# Writes just like the write function but doesn't flush.
		self.stdout.write(string)

		if not ansi: 
			self.auto_position(string)

	def clear_line(self):
		# Clears the current line the cursor is in.
		self.write(colorama.ansi.clear_line())

	def clear_screen(self):
		# Clears the screen by moving the cursor to the end of the terminal screen and calls ansi sequence.
		self.local_cursor.to_pos(self.get_width(), self.get_height()) # Put the cursor at the end of the terminal screen
		self.write(colorama.ansi.clear_screen())
		self.local_cursor.reset_pos()
		self.local_cursor.save_position("Debug", [self.get_width()-1, self.get_height()-1])

	def get_width(self):
		# Get the amount of columns of the terminal (constantly updated automatically)
		return os.get_terminal_size()[0]-1

	def get_height(self):
		# Get the amount of lines of th terminal (constantly updated automatically)
		return os.get_terminal_size()[1]-1