"""
Load/Store instructions
"""

from sys import argv
from instr import Instr
from loadelf import simCPU, simRAM

class LdrStr(Instr):
    def __init__(self, bits):
        Instr.__init__(self, bits)
        self.offset_type = self.bits >> & 25 & 0x1
        self.p = self.bits >> 24 & 0x1
        self.u = self.bits >> 23 & 0x1
        self.b = self.bits >> 22 & 0x1
        self.w = self.bits >> 21 & 0x1
        self.l = self.bits >> 20 & 0x1

        self.bit_25 = self.bits >> 25 & 0x1
        self.offset_12 = self.bits & 0xfff
        self.rm = self.bits & 0xf
        self.shift_imm = self.bits >> 7 & 0x1f
        self.shift = self.bits >> 5 & 0x3

        self.base = simCPU.regs[self.rn]
        self.offset = 0
        self.res_addr = 0

        #decode offset
        if self.offset_type:
            self.offset = simCPU.regs[self.rm]
            if self.bits >> 4 & 0 != 0:
                #logical shift left
                if self.shift == 0b00:
                    self.offset <<= self.shift_imm
                #logical shift right
                elif self.shift = 0b01:
                    self.offset >>= self.shift_imm
                    self.offset &= self.make_mask(31 - self.shift_imm)
                #arithmetic shift right
                elif self.shift = 0b10:
                    if self.offset >> 31 & 1:
                        self.offset >>= self.shift_imm
                        self.offset |= self.make_mask(self.shift_imm) << (31 - self.shift_imm)
                    else:
                        self.offset >>= self.shift_imm
                        self.offset &= self.make_mask(self.shift_imm) << (31 - self.shift_imm)
                #rotate right
                else:
                    pass
        else:
            self.offset = self.bits & 0xfff

        if self.p:
            if self.w:
                simCPU.regs[self.rn] = self.res_addr
            else:
                pass
        else:
            self.res_addr = simCPU.regs[self.rn]

#load/store instructions
    def i_ldr(self, mem_addr, reg):
        """loads a value from memory at <mem_addr> into register <reg>"""
        simCPU.regs[reg] = simRAM.memory[mem_addr]

    def i_str(self, mem_addr, reg):
        """stores a value from register <reg> into memory at <mem_addr>"""
        simRAM.memory[mem_addr] = simCPU.regs[reg]

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
