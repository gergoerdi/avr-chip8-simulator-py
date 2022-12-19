#!/usr/bin/env python2

import sys
from sdl2 import *
import sdl2.ext
import pysimavr.swig.utils as utils

from pysimavr.avr import Avr
from pysimavr.firmware import Firmware

from Board import Board
from Keypad import Keypad
from Screen import Screen
from SPIRAM import SPIRAM

class Chirp8Board(Board):
    def __init__(self, avr):
        Board.__init__(self, avr)

        self.screen = Screen(self)
        self.connect_output(('D', 3), lambda(v): setattr(self.screen, 'sce', v))
        self.connect_output(('D', 5), lambda(v): setattr(self.screen, 'dc', v))
        self.connect_output(('D', 4), lambda(v): setattr(self.screen, 'reset', v))

        self.keypad = Keypad(
            self,
            [('C', 1), ('C', 0), ('B', 2), ('B', 1)],
            [('C', 5), ('C', 4), ('C', 3), ('C', 2)])

        for (i, pin) in enumerate([('C', 5), ('C', 4), ('C', 3), ('C', 2)]):
            def cb(irq, value, i = i):
                if value == 0:
                    print("keypadCols: %d" % i)
            avr.irq.ioport_register_notify(cb, pin)

        self.ram = SPIRAM(self)
        self.connect_output(('D', 6), lambda(v): setattr(self.ram, 'cs', v))

def main():
    avr = Avr(mcu='atmega328p',f_cpu=16000000)
    firmware = Firmware('image.elf')
    avr.load_firmware(firmware)

    sdl2.ext.init()
    board = Chirp8Board(avr)

    running = True
    while running:
        targetTime = SDL_GetTicks() + 17

        board.screen.draw()

        for event in sdl2.ext.get_events():
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_KEYDOWN and event.key.keysym.scancode == SDL_SCANCODE_ESCAPE:
                running = False
                break
        board.keypad.set_keystate(SDL_GetKeyboardState(None))

        while SDL_GetTicks() < targetTime:
            avr.run()

    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
