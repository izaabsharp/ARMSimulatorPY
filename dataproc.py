"""
Data processing instructions
"""

from instr import Instr
from simparts import simCPU, simRAM

class DataProc(Instr):
    def __init__(self, bits):
        Instr.__init__(self, bits)

#all the things that need to be decoded
        self.opcode = 0     #which data-processing instruction is it?
        self.bit_i = 0      #is there an immediate involved?
        self.bit_4 = 0      #immediate shift or register shift?
#the variables that get determined based on the results of the above
        self.imm_8 = 0
        self.rot_imm = 0
        self.shift = 0
        self.shift_imm = 0
        self.rs = 0
        self.rm = 0

#the pieces along the way that need to be determined
        self.is_32bit = False
        self.is_imm_shift = False
        self.is_reg_shift = False
        self.result = 0

#decoding methods
    def get_opcode(self):
        """determine the opcode of a data processing instruction"""
        self.opcode = (self.bits >> 21 & 0xf)

    def set_i(self):
        """determine the i-bit (are we dealing with an immediate or a register?)"""
        self.bit_i = (self.bits >> 25 & 0x1)

    def set_4(self):
        """determine bit 4 (only applicable if <bit_i> is not set)"""
        self.bit_4 = (self.bits >> 4 & 0x1)

    def get_shift_op(self):
        """determine what those last 12 bits are going to do"""
        #32-bit immediate operand 12
        if self.bit_i:
            self.imm_8 = (self.bits & 0xff)
            self.rot_imm = (self.bits >> 8 & 0xf)
            self.is_32bit = True
        #immediate shift operand 12
        elif self.bit_4:
            self.rs = (self.bits >> 12 & 0xf)
            self.shift = (self.bits >> 5 & 0x3)
            self.rm = (self.bits & 0xf)
            self.is_imm_shift = True
        #register shift operand 12
        else:
            self.shift_imm = (self.bits >> 7 & 0x1f)
            self.shift = (self.bits >> 5 & 0x3)
            self.rm = (self.bits & 0xf)
            self.is_reg_shift = True

#methods that affect the <result>
    def set_result(self):
        """change <result> according to shifts to be written to <rd>"""
        if self.is_32bit:
            rot_bits = self.imm_8 & self.make_mask(self.rot_imm*2) << (31-self.rot_imm*2)
            self.result = (self.imm_8 >> (self.rot_imm * 2)) | rot_bits
        elif self.is_imm_shift:
            #logical shift left
            if self.shift == 0x00:
                self.result = simCPU.get_reg(self.rm) << self.shift_imm
            #logical shift right
            elif self.shift == 0x01:
                self.result = simCPU.get_reg(self.rm) >> self.shift_imm
                self.result &= self.make_mask(self.shift_imm) << (31 - self.shift_imm)
            #arithmetic shift right
            elif self.shift == 0x10:
                val = simCPU.get_reg(self.rm)
                if val >> 31 == 1:
                    self.result = (val >> self.shift_imm)
                    self.result |= (self.make_mask(self.shift_imm) << (31 - self.shift_imm))
        elif self.is_reg_shift:
            #logical shift left
            if self.shift == 0x00:
                self.result = simCPU.get_reg(self.rm) << simCPU.get_reg(self.rs)
            #logical shift right
            elif self.shift == 0x01:
                mask = self.make_mask(simCPU.get_reg(self.rs))
                self.result = simCPU.get_reg(self.rm) >> simCPU.get_reg(self.rs)
                self.result &= mask << (31 - (simCPU.get_reg(self.rs) * 2))
            #arithmetic shift right
            elif self.shift == 0x10:
                pass

#the actual data processing instructions
    def i_mov(self):
        """write a value to rd"""
        simCPU.set_reg(self.rd, self.result)

    def i_mvn(self):
        """writes the logical not of a value to rd"""
        pass

    def i_add(self):
        """adds two values together and stores the result in rd"""
        pass

    def i_sub(self):
        """
        subtracts two values and stores the result in rd
        first value from a register
        """
        pass

    def i_rsb(self):
        """
        subtracts two values and stores the result in rd
        second value from a register
        """
        pass

    def i_mul(self):
        pass

    def i_and(self):
        pass

    def i_orr(self):
        pass

    def i_eor(self):
        pass

    def i_bic(self):
        pass

    def i_cmp(self):
        pass

#pythonese switch-case helper thing
    i_instrs = {0b0000: i_and,
                0b0001: i_eor,
                0b0010: i_sub,
                0b0011: i_rsb,
                0b0100: i_add,
                0b1010: i_cmp,
                0b1100: i_orr,
                0b1101: i_mov,
                0b1110: i_bic,
                0b1111: i_mvn}

    def i_execute(self):
        self.set_result()
        self.i_instrs[self.opcode]()
