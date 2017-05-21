"""
Inspect file to see if it is a valid file we want
    Extract any metadata
Load valid file into memory
Set up the RAM and CPU
Go
"""

from sys import argv
import cpu, ram

#ELF file header offsets
"""
Where to find the metadata about the ELF file
"""
E_MAG = (0x00, 4)   #is it even ELF?
E_CLA = (0x04, 1)   #32- or 64-bit?
E_DAT = (0x05, 1)   #big or little endian?
E_ENT = (0x18, 4)   #address of the entry point of process execution
E_PHO = (0x1c, 4)   #start of PHT
E_SHO = (0x20, 4)   #points to the start of the section header table
E_ESZ = (0x2a, 2)   #size of file header
E_PSZ = (0x2a, 2)   #size of a PHT entry
E_PHN = (0x2c, 2)   #number of entries in the PHT 
E_SSZ = (0x2e, 2)   #size of a SHT entry
E_SHN = (0x30, 2)   #number of entries in the SHT
E_SND = (0x32, 2)   #index of the SHT entry that contains the section names

#ELF program header offsets
"""
Found at *E_PHO
Consists of *E_PHN entries
Each entry of size *E_PSZ
"""
P_OFF = (0x04, 4)   #offset into the file image of the program
P_VAD = (0x08, 4)   #virtual address of the segment in memory
P_ADD = (0x0c, 4)   #segment's physical address
P_FSZ = (0x10, 4)   #size of the segment in the file image
P_MSZ = (0x14, 4)   #size of the segment in memory

#ELF section header offsets
"""
Leave these alone for now
Can't remember if I'll need them
"""

#our fake CPU and fake RAM
simCPU = CPU()
simRAM = RAM()

def should_i_even_bother(file_bytes):
    """
    check first 4 bytes of file to see if they are '0x7f''E''L''F'
    return True if so
    return False if not
    """
    if file_bytes[E_MAG[0]:E_MAG[1]] == (str(0x7f) + "ELF"):
        return True
    else:
        return False

if __name__ == "__main__":
    if len(argv) < 2:
        print("usage: loadelf.py [filenames ....]")
    else:
        for arg in argv[1:]:
            elf_file = open(arg, 'rb')
            elf_bytes = elf_file.read()
            pass
    