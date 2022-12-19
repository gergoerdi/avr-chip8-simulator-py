#!/usr/bin/env python2

import sys
from sdl2 import *
import sdl2.ext

from pysimavr.avr import Avr
from pysimavr.firmware import Firmware

from Board import Board

def main():
    avr = Avr(mcu='atmega328p',f_cpu=16000000)
    firmware = Firmware('image.elf')
    avr.load_firmware(firmware)

    sdl2.ext.init()
    board = Board(avr)

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
