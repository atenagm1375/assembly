from tables import *

print(registersx64)
# import re
#
#
# def get_prefixes(mode, state, operand_size, address_size=None):
#     """corresponds to chart no.1 and no.2 of slide 09
#     returns operand prefix, address prefix, and Rex.w or DFlag, respectively."""
#     if mode == 32:
#         if address_size is not None:
#             return operand_size != state and operand_size != 8, address_size != state
#         return operand_size != state and operand_size != 8
#     # TODO add 64bit mode
#
#
# def get_reg_w(mode, name):
#     """corresponds to chart no.3 and no.4 of slide 09
#     returns reg, and w, respectively"""
#     if mode == 32:
#         if name == 'al' or name == 'ax' or name == 'eax':
#             reg = '000'
#         elif name == 'cl' or name == 'cx' or name == 'ecx':
#             reg = '001'
#         elif name == 'dl' or name == 'dx' or name == 'edx':
#             reg = '010'
#         elif name == 'bl' or name == 'bx' or name == 'ebx':
#             reg = '011'
#         elif name == 'ah' or name == 'sp' or name == 'esp':
#             reg = '100'
#         elif name == 'ch' or name == 'bp' or name == 'ebp':
#             reg = '101'
#         elif name == 'dh' or name == 'si' or name == 'esi':
#             reg = '110'
#         elif name == 'bh' or name == 'di' or name == 'edi':
#             reg = '111'
#         else:
#             reg = None
#
#         if name[1] == 'l' or name[1] == 'h':
#             w = '0'
#         else:
#             w = '1'
#         return reg, w
#     # TODO define mode 64bit
#
#
# def get_mode(state, displacement=None, is_memory_ref=True):
#     """corresponds to chart no.5 of slide 09"""
#     if displacement is None and is_memory_ref:
#         return '00'
#     if displacement == 8:
#         return '01'
#     if displacement == state:
#         return '10'
#     if displacement is None and not is_memory_ref:
#         return '11'
#
#
# def get_rm(base, index=None):
#     """corresponds to chart no.6 of slide 09"""
#     if base == 'bx':
#         if index == 'si':
#             return '000'
#         if index == 'di':
#             return '001'
#         if index is None:
#             return '111'
#     if base == 'bp':
#         if index == 'si':
#             return '010'
#         if index == 'di':
#             return '011'
#         if index is None:
#             return '110'
#     if base is None:
#         if index == 'si':
#             return '100'
#         if index == 'di':
#             return '101'
#
#
# def get_condition_code(cond):
#     """corresponds to chart no.7 of slide 09"""
#     if cond == 'o':
#         return '0000'
#     if cond == 'no':
#         return '0001'
#     if cond == 'b' or cond == 'nae':
#         return '0010'
#     if cond == 'nb' or cond == 'ae':
#         return '0011'
#     if cond == 'e' or cond == 'z':
#         return '0100'
#     if cond == 'ne' or cond == 'nz':
#         return '0101'
#     if cond == 'be' or cond == 'na':
#         return '0110'
#     if cond == 'nbe' or cond == 'a':
#         return '0111'
#     if cond == 's':
#         return '1000'
#     if cond == 'ns':
#         return '1001'
#     if cond == 'p' or cond == 'pe':
#         return '1010'
#     if cond == 'np' or cond == 'po':
#         return '1011'
#     if cond == 'l' or cond == 'nge':
#         return '1100'
#     if cond == 'nl' or cond == 'ge':
#         return '1101'
#     if cond == 'le' or cond == 'ng':
#         return '1110'
#     if cond == 'nle' or cond == 'g':
#         return '1111'
#
#
# def get_sib(scale_val, index_reg, base_reg=None):
#     """corresponds to chart no.8, no.9, and no.10 of slide 09"""
#     if scale_val == 1:
#         scale = '00'
#     elif scale_val == 2:
#         scale = '01'
#     elif scale_val == 4:
#         scale = '10'
#     elif scale_val == 8:
#         scale = '11'
#     else:
#         scale = 'error'
#     d = {k[2]: v for k, v in registers_dict32.items()}
#     if index_reg != 'esp':
#         index = d[index_reg]
#     else:
#         index = 'error'
#     if base_reg is not None:
#         base = d[base_reg]
#         return scale, index, base
#     return scale, index
#
#
# def get_index_only(reg):
#     """corresponds to chart no.11 of slide 09"""
#     d = {k[2]: v for k, v in registers_dict32.items() if k[2] != 'esp'}
#     if reg in d.keys():
#         return d[reg]
#     return '100'
#
#
# def compatible_registers(reg1, reg2):
#     if reg1[0] == reg2[0] and reg1[-1] == reg2[-1]:
#         return True
#     if reg1[-1] == reg2[-1]:
#         return True
#     return False
#
#
# def get_operand_size(reg):
#     if reg[-1] == 'h' or reg[-1] == 'l' or reg[-1] == 'b':
#         return 8
#     if reg[0] == 'e' or reg[-1] == 'd':
#         return 32
#     if reg[0] == 'r' and reg[-1] != 'w':
#         return 64
#     return 16
#
#
# def both_registers(mode, arg1, arg2):
#     pre = ''
#     if mode == 32:
#         reg1, w = get_reg_w(mode, arg2)
#         mod = get_mode(mode, is_memory_ref=False)
#         reg2, w = get_reg_w(mode, arg1)
#         if reg1 is None or w is None or mod is None or reg2 is None or not compatible_registers(arg1, arg2):
#             raise ValueError
#         op_pre = get_prefixes(mode, mode, get_operand_size(arg1))
#         if op_pre:
#             pre = '0110 0110 '
#         return pre, w + ' ' + mod + ' ' + reg1 + ' ' + reg2 + '\n'
#
#
# def reg_mem(mode, arg1, arg2):
#     pre = ''
#     reg, w = get_reg_w(mode, arg1)
#     if mode == 32:
#         arg2 = arg2.split('+')
#         if len(arg2) == 1:
#             try:
#                 mem = "{0:b}".format(int(arg2[0]))
#                 a = 4 - int(len(mem) / 8)
#                 for i in range(a):
#                     mem += '0000'
#                 op_pre = get_prefixes(mode, mode, get_operand_size(arg1))
#                 if op_pre:
#                     pre += '0110 0110 '
#             except ValueError:
#                 op_pre, add_pre = get_prefixes(mode, mode, get_operand_size(arg1), get_operand_size(arg2[0]))
#                 if add_pre:
#                     pre += '0110 0111 '
#                 if op_pre:
#                     pre += '0110 0110 '
#                 if get_operand_size(arg2[0]) == 16:
#                     mem = get_rm(arg2[0])
#                     if mem == None:
#                         raise ValueError
#                 elif get_operand_size(arg2[0]) == 32:
#                     mem = get_index_only(arg2[0])
#                     if mem == '100':
#                         raise ValueError
#                 else:
#                     raise ValueError
#             mod = get_mode(mode)
#             return pre, w + ' ' + mod + ' ' + reg + ' ' + mem + '\n'
#         else:
#             regs = [r for r in arg2 if r in reg_list or r.__contains__('*')]
#             disp = sum([int(i) for i in arg2 if i not in regs])
#             if len(regs) > 2:
#                 raise ValueError
#             if len(regs) == 0:
#                 mem = "{0:b}".format(disp)
#             if regs[0].__contains__('*'):
#                 arr = regs[0].split('*')
#                 try:
#                     index = arr[1]
#                     scale = int(arr[0])
#                 except ValueError:
#                     index = arr[0]
#                     scale = int(arr[1])
#                 if len(regs) == 2:
#                     base = regs[1]
#             else:
#                 index = regs[0]
#                 if len(regs) == 2:
#                     if regs[1].__contains__('*'):
#                         raise ValueError
#                     base = regs[1]
#
#
#
# def mov(mode, arg1, arg2):
#     ans = ''
#     if arg1 in reg_list and arg2 in reg_list:
#         pre, post = both_registers(mode, arg1, arg2)
#         ans += pre
#         ans += '1000 100'
#         ans += post
#     elif arg1 in reg_list and arg2[0] == '[':
#         if arg2[-1] != ']':
#             raise ValueError
#         arg2 = arg2.replace('[', '')
#         arg2 = arg2.replace(']', '')
#         arg2 = arg2.replace(' ', '')
#         pre, post = reg_mem(mode, arg1, arg2)
#         ans += pre
#         ans += '1000 101'
#         ans += post
#     return ans
#
#
# def sub(mode, arg1, arg2):
#     pass
#
#
# def xor(mode, arg1, arg2):
#     pass
#
#
# def inc(mode, arg):
#     pass
#
#
# def mul(mode, arg):
#     pass
#
#
# def main():
#     print('--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--')
#     print('Welcome!\nThis is an assembly-to-machine-code converter.\nSimply choose a mode and then write an assembly' +
#           'code operation to get its corresponding machine code.\nWe support the following instructions: \'sub\', ' +
#           '\'mov\', \'xor\', \'inc\', and \'mul\'')
#     print('--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--')
#     while True:
#         print('1. x86\n2. x64\n3. quit')
#         try:
#             mode = int(input('Enter the number of your desired action: '))
#         except ValueError:
#             print('>>> invalid action. Please, try again.')
#             print('...............................................')
#             continue
#
#         if mode == 1:
#             mode = 32
#         elif mode == 2:
#             mode = 64
#         elif mode == 3:
#             print('Good Bye :D')
#             print('...............................................')
#             break
#         else:
#             print('>>> invalid action. Please, try again.')
#             print('...............................................')
#             continue
#
#         invalid = False
#         instructions = input('Enter the instruction and press enter: ').lower()
#         instructions = instructions.replace(' + ', '+')
#         instructions = instructions.replace(' +', '+')
#         instructions = instructions.replace('+ ', '+')
#         instructions = instructions.replace(' * ', '*')
#         instructions = instructions.replace(' *', '*')
#         instructions = instructions.replace('* ', '*')
#         instructions = instructions.split(';')
#         instructions = [re.split(', |,| |\n|\t', instruction) for instruction in instructions if instruction != '']
#         ans = ''
#         for instruction in instructions:
#             if '' in instruction:
#                 instruction.remove('')
#
#             # print(instruction)
#
#             if len(instruction) == 3:
#                 if instruction[0] == 'mov':
#                     try:
#                         ans += mov(mode, instruction[1], instruction[2])
#                     except ValueError:
#                         print('>>> wrong instruction. Please try again.')
#                         print('...............................................')
#                         invalid = True
#                         break
#                 elif instruction[0] == 'sub':
#                     ans += sub(mode, instruction[1], instruction[2])
#                 elif instruction[0] == 'xor':
#                     ans += xor(mode, instruction[1], instruction[2])
#                 else:
#                     print('>>> unsupported or wrong instruction. Please try again.')
#                     print('...............................................')
#                     invalid = True
#                     break
#             elif len(instruction) == 2:
#                 if instruction[0] == 'inc':
#                     ans += inc(mode, instruction[1])
#                 elif instruction[0] == 'mul':
#                     ans += mul(mode, instruction[1])
#                 else:
#                     print('>>> unsupported or wrong instruction. Please try again.')
#                     print('...............................................')
#                     invalid = True
#                     break
#             else:
#                 print('>>> unsupported or wrong instruction. Please try again.')
#                 print('...............................................')
#                 invalid = True
#                 break
#         if invalid:
#             continue
#         print(ans)
#         print('...............................................')
#
#
# reg_values = ['000', '001', '010', '011', '100', '101', '110', '111']
# registers_dict32 = {('ax', 'al', 'eax'): '000', ('cx', 'cl', 'ecx'): '001', ('dx', 'dl', 'edx'): '010',
#                     ('bx', 'bl', 'ebx'): '011', ('sp', 'ah', 'esp'): '100', ('bp', 'ch', 'ebp'): '101',
#                     ('si', 'dh', 'esi'): '110', ('di', 'bh', 'edi'): '111'}
# registers_dict64 = {'r' + k[0]: '0' + v for k, v in registers_dict32.items()}
# for i in range(8, 16):
#     registers_dict64['r' + str(i)] = '1' + reg_values[i - 8]
# reg_list = list(registers_dict64.keys()) + [reg[i] for i in range(3) for reg in registers_dict32]
# main()