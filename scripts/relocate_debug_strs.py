from elftools.elf.elffile import ELFFile
from sys import argv
import struct

if len(argv) < 3:
    print('Usage: {} <input.elf> <output.bin>'.format(argv[0]))
    exit(-1)

offset_list = list()
with open(argv[1], 'rb') as elf_file:
    prog = ELFFile(elf_file)
    rodata = prog.get_section_by_name('.rodata')
    debug_strs = prog.get_section_by_name('debug_strs')

    rodata_offset = rodata.header.sh_addr
    for offset in struct.iter_unpack('i', debug_strs.data()):
        offset_list.append(offset[0] - rodata_offset)


with open(argv[2], 'wb') as offset_file:
    for offset in offset_list:
        offset_file.write(struct.pack('i', offset))
