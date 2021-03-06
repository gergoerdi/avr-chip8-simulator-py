import sdl2.ext
from pysimavr.swig.simavr import avr_alloc_irq
import array

class LCD:
    WIDTH = 84
    HEIGHT = 48

    FG_COLOR = int(sdl2.ext.Color(0xff, 0x00, 0x00, 0x00))
    BG_COLOR = int(sdl2.ext.Color(0xff, 0x73, 0xBD, 0x71))
    
    def __init__(self, board):
        self.board = board

        self.sce = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        self.dc = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        self.reset = avr_alloc_irq(board.avr.irq_pool, 0, 1, None)
        
        self.dirty = False
        self.pixbuf = array.array('I', [0 for i in range(self.WIDTH * self.HEIGHT)])
        self.nextXY = (0, 0)

    def draw(self):
        return self.pixbuf

    def mosi(self, value):
        if self.sce.value != 0:
            return
            
        if self.dc.value == 0:
            #print "Command to LCD: 0x%02x" % value
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
