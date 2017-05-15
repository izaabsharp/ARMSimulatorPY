"""
Inspect file to see if it is a valid file we want
    Extract any metadata
Load valid file into memory
Set up the RAM and CPU
Go
"""

from sys import argv
import cpu, ram

simCPU = CPU()
simRAM = RAM()

def is_elf(in_file):
    """
    check first 4 bytes of file to see if they are '0x7f''E''L''F'
    return True if so
    return False if not
    """
    elf_bits = in_file.read(4)
    if elf_bits == (str(0x7f) + "ELF"):
        return True
    else:
        return False

if __name__ == "__main__":
    pass
    