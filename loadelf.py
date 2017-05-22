"""
Inspect file to see if it is a valid file we want
    Extract any metadata
Load valid file into memory
Set up the RAM and CPU
Go
"""

from sys import argv
from cpu import CPU
from ram import RAM

#ELF file header offsets
"""
Where to find the metadata about the ELF file
(Offset within ELF file, location to which the piece goes)
"""
E_MAG = (0x00, 0x04)   #is it even ELF?
E_BIT = (0x04, 0x05)   #32- or 64-bit?
E_END = (0x05, 0x06)   #big or little endian?
E_ENT = (0x18, 0x1c)   #address of the entry point of process execution
E_PHO = (0x1c, 0x20)   #start of PHT
E_SHO = (0x20, 0x24)   #points to the start of the section header table
E_ESZ = (0x28, 0x2a)   #size of file header
E_PSZ = (0x2a, 0x2c)   #size of a PHT entry
E_PHN = (0x2c, 0x2e)   #number of entries in the PHT

#ELF program header offsets
"""
Found at *E_PHO
Consists of *E_PHN entries
Each entry of size *E_PSZ
"""
P_OFF = (0x04, 0x08)   #offset into the file image of the program
P_VAD = (0x08, 0x0c)   #virtual address of the segment in memory
P_ADD = (0x0c, 0x10)   #segment's physical address
P_FSZ = (0x10, 0x14)   #size of the segment in the file image
P_MSZ = (0x14, 0x18)   #size of the segment in memory

#our fake CPU and fake RAM
simCPU = CPU()
simRAM = RAM()

def should_i_even_bother(file_bytes):
    """
    check first 4 bytes of file to see if they are '0x7f''E''L''F'
    check to see if 32-bit
    check to see if little endian
        return True if all conditions hold
        return False if any do not
    """
    if file_bytes[E_MAG[0]:E_MAG[1]] == (str(0x7f) + "ELF"):
        if file_bytes[E_BIT[0]] == 1:
            if file_bytes[E_END[0]] == 1:
                return True #this is a 32-bit little-endian ELF file
    return False #this is not a 32-bit little-endian ELF file

def parse_pht(file_bytes):
    """
    parse out the different pieces of the program header table 
    that we will need in order to store the program in RAM
    """
    ph_off = file_bytes[E_PHO[0]:E_PHO[1]]  #offset of PHT
    ph_siz = file_bytes[E_PSZ[0]:E_PSZ[1]]  #size of PHT
    ph_num = file_bytes[E_PHN[0]:E_PHN[1]]  #number of PHTs
    for i in range(ph_num):
        p_addr = file_bytes[(ph_off + (ph_siz * i) + P_OFF[0]):P_OFF[1]]    #address of program within the file image
        p_size = file_bytes[(ph_off + (ph_siz * i) + P_FSZ[0]):P_FSZ[1]]    #size of the program within the file image 
        v_addr = file_bytes[(ph_off + (ph_siz * i) + P_VAD[0]):P_VAD[1]]    #virtual address of the program out in RAM
        v_size = file_bytes[(ph_off + (ph_siz * i) + P_MSZ[0]):P_MSZ[1]]    #size of the program out in RAM
        simRAM.memory[v_addr:(v_addr + v_size)] = file_bytes[p_addr:(p_addr + p_size)]

if __name__ == "__main__":
    if len(argv) < 2:
        print("usage: loadelf.py [filenames ....]")
        exit()

    for arg in argv[1:]:
        elf_file = open(arg, 'rb')
        elf_bytes = elf_file.read()
        if should_i_even_bother(elf_bytes) == False:
            continue
        parse_pht(elf_bytes)
