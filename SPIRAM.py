class SPIRAM:
    CMD_INIT = 0x01
    CMD_WRITE = 0x02
    CMD_READ = 0x03
    
    def __init__(self, board):
        self.ram = [0 for i in range(8 * 1024)]

        self.cs = True
        board.avr.irq.ioport_register_notify(self.irq_cb, ('D', 6))

        self.addr = 0
        self.state = self.COMMAND

    def irq_cb(self, irq, value):
        if irq.irq == 6:
            self.cs = value
            

    def mosi(self, value):
        if self.cs:
            return

        print "SPIRAM: %02x" % value
        self.state(value)
        

    def COMMAND(self, value):
        self.command = value
        if self.command == self.CMD_INIT:
            self.state = self.PARAM
        else:
            self.state = self.ADDR1

    def PARAM(self, value):
        if self.command == self.CMD_WRITE:
            print "ADDR = 0x%04x, VALUE <= 0x%02x" % (addr, value)
            self.ram[addr] = value
        elif self.command == self.CMD_READ:
            print "ADDR = 0x%04x, VALUE => 0x%02x" % (addr, self.ram[addr])
            self.board.miso(self.ram[addr])
        self.state = self.COMMAND

    def ADDR1(self, value):
        self.addr = (addr << 8) + value
        self.state = self.ADDR2

    def ADDR2(self, value):
        self.addr = (addr << 8) + value
        self.state = self.PARAM

