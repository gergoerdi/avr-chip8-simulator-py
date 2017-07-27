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
        avr_connect_irq(avr.irq.getioport(('D', 3)), self.lcd.sce)
        avr_connect_irq(avr.irq.getioport(('D', 5)), self.lcd.dc)
        avr_connect_irq(avr.irq.getioport(('D', 4)), self.lcd.reset)
        
        self.keypad = Keypad(self)

        self.ram = SPIRAM(self)
        avr_connect_irq(avr.irq.getioport(('D', 6)), self.ram.cs)
        

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
