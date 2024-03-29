class SPIRAM:
    CMD_INIT = 0x01
    CMD_WRITE = 0x02
    CMD_READ = 0x03
    
    def __init__(self, board):
        self.ram = [0 for i in range(8 * 1024)]

        self.cs = 1
        self.miso = board.connect_mosi(self.mosi)

        self.addr = 0
        self.state = self.COMMAND

    def mosi(self, value):
        if self.cs != 0:
            return
        self.state(value)
        

    def COMMAND(self, value):
        self.command = value
        if self.command == self.CMD_INIT:
            self.state = self.PARAM
        else:
            self.state = self.ADDR1

    def PARAM(self, value):
        if self.command == self.CMD_WRITE:
            print("ADDR = 0x%04x, VALUE <= 0x%02x" % (self.addr, value))
            self.ram[self.addr] = value
        elif self.command == self.CMD_READ:
            print("ADDR = 0x%04x, VALUE => 0x%02x" % (self.addr, self.ram[self.addr]))
            self.miso(self.ram[self.addr])
        self.state = self.COMMAND

    def ADDR1(self, value):
        self.addr = ((self.addr << 8) + value) & 0x1fff
        self.state = self.ADDR2

    def ADDR2(self, value):
        self.addr = ((self.addr << 8) + value) & 0x1fff
        self.state = self.PARAM

