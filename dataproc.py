"""
Data processing instructions
"""

from sys import argv
from instr import Instr
from loadelf import simCPU

class DataProc(Instr):
    """
    Class for Data Processing Instructions
    Inherits from Instr class
    """
    def __init__(self, bits):
        Instr.__init__(self, bits)
        #what data processing instruction is it?
        self.opcode = self.bits >> 21 & 0xf
        #is there an immediate involved?
        self.bit_i = self.bits >> 25 & 0x1
        #is it an immediate or a register shift?
        self.bit_4 = self.bits >> 4 & 0x1
        #the variables that get determined based on the results of the above
        self.imm_8 = self.bits & 0xff
        self.rot_imm = self.bits >> 8 & 0xf
        self.shift = self.bits >> 5 & 0x3
        self.shift_imm = self.bits >> 7 & 0x1f
        self.rs = self.bits >> 8 & 0xf
        self.rm = self.bits & 0xf
        #the pieces along the way that need to be determined
        self.is_32bit = False
        self.is_imm_shift = False
        self.is_reg_shift = False
        self.result = 0

        #32-bit immediate operand 12
        if self.bit_i:
            self.is_32bit = True
        #register shift operand 12
        elif self.bit_4:
            self.is_reg_shift = True
        #immediate shift operand 12
        else:
            self.is_imm_shift = True

    def set_result(self):
        """change <result> according to shifts"""
        #rotating right to create immediate value
        if self.is_32bit:
            rot_bits = (self.imm_8 & self.make_mask(self.rot_imm*2)) << (31-self.rot_imm*2)
            self.result = (self.imm_8 >> (self.rot_imm * 2)) | rot_bits
        #shifting by immediate value
        elif self.is_imm_shift:
            #logical shift left
            if self.shift == 0b00:
                self.result = simCPU.regs[self.rm] << self.shift_imm
            #logical shift right
            elif self.shift == 0b01:
                self.result = simCPU.regs[self.rm] >> self.shift_imm
                self.result &= self.make_mask(31 - self.shift_imm)
            #arithmetic shift right
            elif self.shift == 0b10:
                #retrieve source value
                val = simCPU.regs[self.rm]
                #MSB is set
                if val >> 31 == 1:
                    #shift source value
                    self.result = val >> self.shift_imm
                    #set shifted in bits
                    self.result |= self.make_mask(self.shift_imm) << (31 - self.shift_imm)
                #MSB is not set (basically a logical shift right)
                else:
                    #shift source value
                    self.result = val >> self.shift_imm
                    #clear shifted in bits
                    self.result &= self.make_mask(31 - self.shift_imm)
            #rotate right
            elif self.shift == 0b11:
                pass
        #shifting by value found in <rs>
        elif self.is_reg_shift:
            #logical shift left
            if self.shift == 0b00:
                self.result = simCPU.regs[self.rm] << simCPU.regs[self.rs]
            #logical shift right
            elif self.shift == 0b01:
                self.result = simCPU.regs[self.rm] >> simCPU.regs[self.rs]
                self.result &= self.make_mask(31 - simCPU.regs[self.rs])
            #arithmetic shift right
            elif self.shift == 0b10:
                res_val = simCPU.regs[self.rm]
                shift_val = simCPU.regs[self.rs]
                if res_val >> 31 == 1:
                    #shift source value
                    self.result = res_val >> shift_val
                    #set shifted in bits
                    self.result |= self.make_mask(shift_val) << (31 - shift_val)
                else:
                    #shift source value
                    self.result = res_val >> shift_val
                    #clear shifted in bits
                    self.result &= self.make_mask(31 - shift_val)
            #rotate right
            elif self.shift == 0b11:
                pass

#the actual data processing instructions
    def i_mov(self):
        """write a value to <rd>"""
        simCPU.regs[self.rd] = self.result

    def i_mvn(self):
        """write the logical not of a value to <rd>"""
        simCPU.regs[self.rd] = ~self.result

    def i_add(self):
        """adds two values together and stores the result in rd"""
        simCPU.regs[self.rd] = simCPU.regs[self.rn] + self.result

    def i_sub(self):
        """
        subtracts two values and stores the result in rd
        first operand from a register
        """
        simCPU.regs[self.rd] = simCPU.regs[self.rn] - self.result

    def i_rsb(self):
        """
        subtracts two values and stores the result in rd
        second value from a register
        """
        simCPU.regs[self.rd] = self.result - simCPU.regs[self.rn]

    def i_mul(self):
        """
        multiply 2 values and store result in <rd>
        (rd bits where rn bits typically are in a data processing instruction)
        """
        simCPU.regs[self.rn] = simCPU.regs[self.rm] * simCPU.regs[self.rs]

    def i_and(self):
        """perform a bitwise AND of two values and store result in <rd>"""
        simCPU.regs[self.rd] = simCPU.regs[self.rn] & self.result

    def i_orr(self):
        """perform a bitwise OR of two values and store result in <rd>"""
        simCPU.regs[self.rd] = simCPU.regs[self.rn] & self.result

    def i_eor(self):
        """perform a bitwise XOR of two values and store result in <rd>"""
        simCPU.regs[self.rd] = simCPU.regs[self.rn] ^ self.result

    def i_bic(self):
        """
        perform a bitwise AND of one value with the complement of another
        store the result in <rd>
        """
        simCPU.regs[self.rd] = simCPU.regs[self.rn] & ~self.result

    def i_cmp(self):
        pass

#function dictionary that matches opcodes to the data processing instruction functions
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

#method to execute the decoded instruction
    def i_execute(self):
        self.set_result()
        #check for MUL instruction
        if self.check_mul():
            self.i_mul()
        else:
            self.i_instrs[self.opcode](self)

if __name__ == "__main__":
    simCPU.regs[0], simCPU.regs[1] = 0x2, 0xe
    for arg in argv[1:]:
        test_instr = DataProc(int(arg, 0))
        test_instr.i_execute()
        print(simCPU.regs)
