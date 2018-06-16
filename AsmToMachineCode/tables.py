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


opcode = {'mov': {'r/m,r': '1000100w', 'r,m': '1000101w', 'r/m,d': '1100011w'},
          'sub': {'r/m,r': '0010100w', 'r,m': '0010101w', 'r/m,d': '001011sw'},
          'xor': {'r/m,r': '0011000w', 'r,m': '0011001w', 'r/m,d': '001101sw'},
          'mul': {'r': '1111011w11100'},
          'not': {'r': '1111011w11010'}}


Rex = '0100wrxb'
