"""
Load/Store instructions
"""

from instr import Instr
from simparts import simCPU, simRAM

class LdrStr(Instr):
    def __init__(self, bits):
        Instr.__init__(self, bits)
        self.p = self.bits >> 24 & 0x1
        self.u = self.bits >> 23 & 0x1
        self.b = self.bits >> 22 & 0x1
        self.w = self.bits >> 21 & 0x1
        self.l = self.bits >> 20 & 0x1

#determine how PUBWL will affect the outcome

#load/store instructions
    def i_ldr(self, mem_addr, reg):
        """loads a value from memory at <mem_addr> into register <reg>"""
        pass

    def i_str(self, mem_addr, reg):
        """stores a value from register <reg> into memory at <mem_addr>"""
        pass

    def i_stm(self):
        pass

    def i_ldm(self):
        pass

    def i_execute(self):
        if self.l:
            self.i_ldr()
        else:
            self.i_str()

if __name__ == '__main__':
    pass
