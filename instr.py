"""
Generic instruction class from which others inherit
"""

class Instr:
    def __init__(self, bits):
        self.bits = bits
        self.rn = 0
        self.rd = 0

    def make_mask(self, num_ones):
        """create a mask of 1s length <num_ones>"""
        res = 0
        for i in range(num_ones):
            res |= (1 << i)
        return res

    def get_rn(self):
        """determine the source register number"""
        self.rn = (self.bits >> 16 & 0xf)

    def get_rd(self):
        """determine the destination register number"""
        self.rd = (self.bits >> 12 & 0xf)

    def i_execute(self):
        """
        generic instruction execution method to be
        filled in by child classes
        """
        pass
