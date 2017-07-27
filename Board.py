from pysimavr.avr import Avr
from pysimavr.connect import avr_connect_irq
import pysimavr.swig.utils as utils
from pysimavr.swig.simavr import avr_raise_irq

from Keypad import Keypad
from LCD import LCD
from SPIRAM import SPIRAM

class Board:
    def __init__(self, avr):
        self.avr = avr
        self.lcd = LCD(self)
        self.keypad = Keypad(self)
        self.ram = SPIRAM(self)

        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        self.miso(0)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        # print "miso: %s" % value
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        # print("mosi: %s" % value)
        self.lcd.mosi(value)
        self.ram.mosi(value)
