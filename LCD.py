import sdl2.ext

class LCD:
    WIDTH = 84
    HEIGHT = 48

    FG_COLOR = sdl2.ext.Color(0xff, 0x00, 0x00, 0x00)
    BG_COLOR = sdl2.ext.Color(0xff, 0x73, 0xBD, 0x71)
    
    def __init__(self, board):
        self.framebuf = [[False for i in range(self.HEIGHT)] for i in range(self.WIDTH)]
        self.framebuf[10][10] = True
        pass

    def draw(self, pixels):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                pixels[y * self.WIDTH + x] = int(self.FG_COLOR if self.framebuf[x][y] else self.BG_COLOR)
        pass
        

    def mosi(self, value):
        pass
