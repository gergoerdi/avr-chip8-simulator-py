from pysimavr.avr import Avr
from pysimavr.connect import avr_connect_irq

from Keypad import Keypad
from LCD import LCD

class Board:
    def __init__(self, avr):
        self.avr = avr
        self.lcd = LCD()
        self.keypad = Keypad()

        avr.irq.spi_register_notify(self.mosi)

    def mosi(self, irq, val):
        print("mosi: %s" % val)
