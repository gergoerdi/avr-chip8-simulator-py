from pysimavr.swig.simavr import avr_alloc_irq, avr_raise_irq
from sdl2 import *

import sys

class Keypad:
    keymap = {
        SDL_SCANCODE_1: (0, 0),
        SDL_SCANCODE_2: (0, 1),
        SDL_SCANCODE_3: (0, 2),
        SDL_SCANCODE_4: (0, 3),

        SDL_SCANCODE_Q: (1, 0),
        SDL_SCANCODE_W: (1, 1),
        SDL_SCANCODE_E: (1, 2),
        SDL_SCANCODE_R: (1, 3),

        SDL_SCANCODE_A: (2, 0),
        SDL_SCANCODE_S: (2, 1),
        SDL_SCANCODE_D: (2, 2),
        SDL_SCANCODE_F: (2, 3),

        SDL_SCANCODE_Z: (3, 0),
        SDL_SCANCODE_X: (3, 1),
        SDL_SCANCODE_C: (3, 2),
        SDL_SCANCODE_V: (3, 3)
    }

    def __init__(self, board):
        self.keystate = [[False for i in range(4)] for i in range(4)]
        self.rows = [avr_alloc_irq(board.avr.irq_pool, 0, 1, None) for i in range(4)]
        self.cols = [avr_alloc_irq(board.avr.irq_pool, 0, 1, None) for i in range(4)]
        self.row_selected = [False for row in self.rows]

        for (i, row) in enumerate(self.rows):
            board.avr.irq._register_callback(row, lambda irq, value, i=i: self.scan_row(i, value), True)

    def set_keystate(self, keystate):
        for (scancode, (row, col)) in self.keymap.items():
            self.keystate[row][col] = keystate[scancode]

    def scan_row(self, i, value):
        self.row_selected[i] = (value == 0)

        for (j, col) in enumerate(self.cols):
            found = False
            for (i, row) in enumerate(self.rows):
                if self.row_selected[i]:
                    found = found or self.keystate[i][j]
            avr_raise_irq(col, 0 if found else 1)
