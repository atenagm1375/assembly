registersx86 = {'al': '000', 'ax': '000', 'eax': '000',
                'cl': '001', 'cx': '001', 'ecx': '001',
                'dl': '010', 'dx': '010', 'edx': '010',
                'bl': '011', 'bx': '011', 'ebx': '011',
                'ah': '100', 'sp': '100', 'esp': '100',
                'ch': '101', 'bp': '101', 'ebp': '101',
                'dh': '110', 'si': '110', 'esi': '110',
                'bh': '111', 'di': '111', 'edi': '111'}


registersx64 = {k: '0' + v for k, v in registersx86.items()}

for k in registersx86.keys():
    if len(k) == 3:
        new_k = k[:]
        new_k = new_k.replace('e', 'r')
        registersx64[new_k] = '0' + registersx86[k]

for i in range(8, 16):
    registersx64['r' + str(i) + 'b'] = '1' + '{0:03b}'.format(i - 8)
    registersx64['r' + str(i) + 'w'] = '1' + '{0:03b}'.format(i - 8)
    registersx64['r' + str(i) + 'd'] = '1' + '{0:03b}'.format(i - 8)
    registersx64['r' + str(i)] = '1' + '{0:03b}'.format(i - 8)


rmx86 = {('bx', 'si'): '000', ('bx', 'di'): '001', ('bp', 'si'): '010', ('bp', 'di'): '011',
         (None, 'si'): '100', (None, 'di'): '101', ('bp', None): '110', ('bx', None): '111'}


opcode = {'mov': {'rr': '1000100w', 'mr': '1000100w', 'rm': '1000101w', 'rd': '1100011w', 'md': '1100011w', 'op': '000'},
          'sub': {'rr': '0010100w', 'mr': '0010100w', 'rm': '0010101w', 'rd': '1000001w', 'md': '1000001w', 'op': '101'},
          'xor': {'rr': '0011000w', 'mr': '0011000w', 'rm': '0011001w', 'rd': '1000001w', 'md': '1000001w', 'op': '110'},
          'mul': {'r': '1111011w11100', 'm': '1111011w00100'},
          'not': {'r': '1111011w11010', 'm': '1111011w00010'}}


Rex = '0100wrxb'


operand_prefix = '01100110'


address_prefix = '01100111'


size = (8, 16, 32, 64, 80, 128, 256)


mod = ('00', '01', '10', '11')


scale = {'1': '00', '2': '01', '4': '10', '8': '11'}


instruction_size_set = {'byte': size[0], 'dword': size[2], 'qword': size[3], 'word': size[1]}


bad_expression_msg = 'Bad expression! Please try again.'
both_mem_msg = 'Both arguments cannot be a memory! Please try again.'
invalid_num_of_args_msg = 'Invalid number of arguments! Please try again.'
ambiguous_operand_size_msg = 'Ambiguous operand size! Please try again.'
