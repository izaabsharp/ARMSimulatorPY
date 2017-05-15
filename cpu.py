"""
Central Processing Unit
    registers
    fetch/decode/execute cycle
    instruction counter
"""

from instr import Instr

class CPU:
    """The CPU class"""
    def __init__(self):
        self.regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.instr_count = 0

    def fetch(self):
        """retrieves the 32-bit instruction at the address contained in pc (i.e. regs[15])"""
        self.instr_count += 1
        return 0

    def decode(self):
        """decode the instruction at address retrieved from pc"""
        instr = self.fetch()

    def execute(self):
        """execute the instruction"""
        pass

    def cycle(self):
        self.decode()
        self.execute()

if __name__ == "__main__":
    pass
