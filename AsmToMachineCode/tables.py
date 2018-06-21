from constants import *


def get_register_size(reg):
    if reg is None:
        return 0
    if reg[0] == 'e':
        return size[2]
    if reg[0] == 'r':
        return size[3]
    if reg[-1] == 'l' or reg[-1] == 'h':
        return size[0]
    return size[1]


def isNumber(s):
    if (s[:2] == '0x' and s[2:].isdigit()) or s.isdigit():
        return True
    return False


def has_operand_prefix(arch, state, op_size):
    if arch == size[2]:
        return state != op_size and op_size != size[0]
    return op_size == size[1]


def has_address_prefix(arch, state, add_size):
    if arch == size[2]:
        return state != add_size
    if add_size <= size[1]:
        return None
    return add_size == size[2]


def get_w(reg_size):
    if reg_size == size[0]:
        return 0
    return 1


def get_mod(disp_size, is_mem=True):
    if disp_size == size[0]:
        return mod[1]
    if disp_size == size[1] or disp_size == size[2]:
        return mod[2]
    if is_mem:
        return mod[0]
    if not is_mem:
        return mod[3]


def get_reg_rm(arch, index, base=None):
    index_size = get_register_size(index)
    base_size = get_register_size(base)
    if arch == size[2]:
        if index_size == size[1] and (base is None or base_size == size[1]):
            return rmx86[index][base]
        if base_size == 0 and index_size == size[2]:
            return registersx86[index]
        if base_size == size[2] and index_size == size[2]:
            return '100'
    if arch == size[3]:
        if base_size == 0 and index_size > size[1]:
            return registersx86[index]
        if base_size == size[2] and index_size == size[2]:
            return '100'
