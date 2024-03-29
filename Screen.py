import sdl2.ext
from sdl2 import *
from pysimavr.swig.simavr import avr_alloc_irq
import array
import ctypes

class Screen:
    WIDTH = 84
    HEIGHT = 48

    FG_COLOR = int(sdl2.ext.Color(0xff, 0x00, 0x00, 0x00))
    BG_COLOR = int(sdl2.ext.Color(0xff, 0x73, 0xBD, 0x71))
    
    def __init__(self, board):
        self.sce = 1
        self.dc = 1
        self.reset = 1
        board.connect_mosi(self.mosi)
        
        self.dirty = False
        self.pixbuf = array.array('I', [0 for i in range(self.WIDTH * self.HEIGHT)])
        self.nextXY = (0, 0)

        self.window = sdl2.ext.Window("CHIRP-328", size=(self.WIDTH * 8, self.HEIGHT * 8))
        self.renderer = SDL_CreateRenderer(self.window.window, -1, SDL_RENDERER_ACCELERATED)
        SDL_RenderSetLogicalSize(self.renderer, self.WIDTH * 8, self.HEIGHT * 8)
        self.texture = SDL_CreateTexture(
            self.renderer, SDL_PIXELFORMAT_RGB888, SDL_TEXTUREACCESS_STREAMING,
            self.WIDTH, self.HEIGHT)
        self.window.show()

    def draw(self):
        buffer = (ctypes.c_uint32 * (self.HEIGHT * self.WIDTH))(*self.pixbuf)
        SDL_UpdateTexture(self.texture, None, buffer, self.WIDTH * 4)
        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)

    def mosi(self, value):
        if self.sce != 0:
            return
            
        if self.dc == 0:
            print "Command to screen: 0x%02x" % value
            pass
        else:
            (x, y) = self.nextXY
            for i in range(8):
                self.pixbuf[x + (y + i) * self.WIDTH] = self.FG_COLOR if value & 0x01 else self.BG_COLOR
                value = value >> 1
            self.dirty = True

            y = y + 8
            if y >= self.HEIGHT:
                (x, y) = (x + 1, 0)
            if x >= self.WIDTH:
                (x, y) = (0, 0)
            self.nextXY = (x, y)
