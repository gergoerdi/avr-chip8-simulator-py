from Keypad import Keypad
from LCD import LCD

class Board:
    def __init__(self):
        self.lcd = LCD()
        self.keypad = Keypad()
