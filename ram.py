"""
Where all the memory of the elf file exists
"""

class RAM:
    """The memory of the system"""
    def __init__(self):
        self.memory = []

    def read_mem(self, addr):
        """read the 32-bit instruction from memory at address addr"""
        return self.memory[addr]

    def write_mem(self, addr, val):
        """set the 32-bit contents at memory address <addr> at <addr> to <val>"""
        self.memory[addr] = val
