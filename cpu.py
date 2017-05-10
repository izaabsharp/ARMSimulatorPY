"""
Central Processing Unit
Where the registers live and all methods for register
    access/modification exist
"""

from simparts import simRAM

class CPU:
    """The CPU class"""
    def __init__(self):
        self.regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.instr_count = 0

    def get_reg(self, regnum):
        """return the value in register <regnum>"""
        return self.regs[regnum]

    def set_reg(self, regnum, val):
        """set value in register <regnum> to <val>"""
        self.regs[regnum] = val

    def fetch(self):
        """retrieves the 32-bit instruction at the address contained in pc (i.e. regs[15])"""
        self.instr_count += 1
        return simRAM.read_mem(self.regs[15])

    def decode(self):
        """decode the instruction at address retrieved from pc"""
        instr = self.fetch()

    def execute(self):
        """execute the instruction"""
        pass

    def cycle(self):
        self.decode()
        self.execute()
