from pysimavr.avr import Avr
from pysimavr.swig.simavr import avr_alloc_irq, avr_raise_irq
from pysimavr.connect import avr_connect_irq
import pysimavr.swig.utils as utils

from Keypad import Keypad
from Screen import Screen
from SPIRAM import SPIRAM

class Board:
    def __init__(self, avr):
        self.avr = avr
        self.mosi_callbacks = []

        self.screen = Screen(self)
        self.connect_output(('D', 3), self.screen.sce)
        self.connect_output(('D', 5), self.screen.dc)
        self.connect_output(('D', 4), self.screen.reset)
        
        self.keypad = Keypad(self)
        for (pin, row) in zip([('C', 1), ('C', 0), ('B', 2), ('B', 1)], self.keypad.rows):
            avr_connect_irq(avr.irq.getioport(pin), row)
        for (pin, col) in zip([('C', 5), ('C', 4), ('C', 3), ('C', 2)], self.keypad.cols):
            avr_connect_irq(col, avr.irq.getioport(pin))

        for (i, pin) in enumerate([('C', 5), ('C', 4), ('C', 3), ('C', 2)]):
            def cb(irq, value, i = i):
                if value == 0:
                    print("keypadCols: %d" % i)
            avr.irq.ioport_register_notify(cb, pin)

        self.ram = SPIRAM(self)
        avr_connect_irq(avr.irq.getioport(('D', 6)), self.ram.cs)

        self.misoirq = avr.irq.getspi(0, utils.SPI_IRQ_INPUT)
        self.miso(0)
        avr.irq.spi_register_notify(self.mosi)

    def miso(self, value):
        avr_raise_irq(self.misoirq, value)
        
    def mosi(self, irq, value):
        for cb in self.mosi_callbacks:
            cb(value)

    def connect_input(self, pin):
        irq = avr_alloc_irq(self.avr.irq_pool, 0, 1, None)
        avr_connect_irq(irq, self.avr.irq.getioport(pin))
        return lambda(val): avr_raise_irq(irq, val)

    def create_output(self):
        return avr_alloc_irq(self.avr.irq_pool, 0, 1, None)

    def connect_output(self, pin, listener):
        avr_connect_irq(self.avr.irq.getioport(pin), listener)

    def connect_mosi(self, cb):
        self.mosi_callbacks += [cb]
        return self.miso
