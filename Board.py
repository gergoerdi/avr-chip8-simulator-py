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
        for (pin, row) in zip([('C', 1), ('C', 0), ('B', 2), ('B', 1)], self.keypad.rows):
            avr_connect_irq(avr.irq.getioport(pin), row)
        for (pin, col) in zip([('C', 5), ('C', 4), ('C', 3), ('C', 2)], self.keypad.cols):
            avr_connect_irq(col, avr.irq.getioport(pin))

        # for (i, col) in enumerate(self.keypad.cols):
        #     def cb(irq, value, i = i):
        #         if value == 0:
        #             print "keypadCols: %d" % i
        #     avr.irq._register_callback(col, cb, True)
            
        for (i, pin) in enumerate([('C', 5), ('C', 4), ('C', 3), ('C', 2)]):
            def cb(irq, value, i = i):
                if value == 0:
                    print "keypadCols: %d" % i
            avr.irq.ioport_register_notify(cb, pin)

        self.ram = SPIRAM(self)
        avr_connect_irq(avr.irq.getioport(('D', 6)), self.ram.cs)

        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        self.miso(0)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        self.lcd.mosi(value)
        self.ram.mosi(value)
