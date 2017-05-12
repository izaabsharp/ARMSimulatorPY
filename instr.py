"""
Generic instruction class from which others inherit
"""

class Instr:
    def __init__(self, bits):
        self.bits = bits
        #source register
        self.rn = self.bits >> 16 & 0xf
        #destination register number
        self.rd = self.bits >> 12 & 0xf

    def make_mask(self, num_ones):
        """create a mask of 1s length <num_ones>"""
        res = 0
        for i in range(num_ones):
            res |= (1 << i)
        return res

    def check_mul(self):
        """
        check bits 25, 7, and 4 to see if the instruction
        is masquerading as a MUL instruction
        """
        if self.bits >> 25 & 1 == 0:
            if self.bits >> 7 & 1 == 1:
                if self.bits >> 4 & 1 == 1:
                    return True

    def i_execute(self):
        """
        generic instruction execution method to be
        filled in by child instruction classes
        """
        pass
