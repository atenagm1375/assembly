import re


def get_dflagrexw_prefixes(mode, operand_size, address_size, state=None):
    """corresponds to chart no.1 and no.2 of slide 09
    returns operand prefix, address prefix, and Rex.w or DFlag, respectively."""
    if mode == 32:
        if state == 32:
            dflag = 1
        else:
            dflag = 0
        return dflag, operand_size != state, address_size != state
    # TODO add 64bit mode


def get_reg_w(mode, name):
    """corresponds to chart no.3 and no.4 of slide 09
    returns reg, and w, respectively"""
    if mode == 32:
        if name == 'al' or name == 'ax' or name == 'eax':
            reg = '000'
        elif name == 'cl' or name == 'cx' or name == 'ecx':
            reg = '001'
        elif name == 'dl' or name == 'dx' or name == 'edx':
            reg = '010'
        elif name == 'bl' or name == 'bx' or name == 'ebx':
            reg = '011'
        elif name == 'ah' or name == 'sp' or name == 'esp':
            reg = '100'
        elif name == 'ch' or name == 'bp' or name == 'ebp':
            reg = '101'
        elif name == 'dh' or name == 'si' or name == 'esi':
            reg = '110'
        elif name == 'bh' or name == 'di' or name == 'edi':
            reg = '111'
        else:
            reg = None

        if name[1] == 'l' or name[1] == 'h':
            w = 0
        else:
            w = 1
        return reg, w
    # TODO define mode 64bit


def get_mode(state, displacement=None, is_memory_ref=True):
    """corresponds to chart no.5 of slide 09"""
    if displacement is None and is_memory_ref:
        return '00'
    if displacement == 8:
        return '01'
    if displacement == state:
        return '10'
    if displacement is None and not is_memory_ref:
        return '11'


def get_rm(base, index=None):
    """corresponds to chart no.6 of slide 09"""
    if base == 'bx':
        if index == 'si':
            return '000'
        if index == 'di':
            return '001'
        if index is None:
            return '111'
    if base == 'bp':
        if index == 'si':
            return '010'
        if index == 'di':
            return '011'
        if index is None:
            return '110'
    if base is None:
        if index == 'si':
            return '100'
        if index == 'di':
            return '101'


def get_condition_code(cond):
    """corresponds to chart no.7 of slide 09"""
    if cond == 'o':
        return '0000'
    if cond == 'no':
        return '0001'
    if cond == 'b' or cond == 'nae':
        return '0010'
    if cond == 'nb' or cond == 'ae':
        return '0011'
    if cond == 'e' or cond == 'z':
        return '0100'
    if cond == 'ne' or cond == 'nz':
        return '0101'
    if cond == 'be' or cond == 'na':
        return '0110'
    if cond == 'nbe' or cond == 'a':
        return '0111'
    if cond == 's':
        return '1000'
    if cond == 'ns':
        return '1001'
    if cond == 'p' or cond == 'pe':
        return '1010'
    if cond == 'np' or cond == 'po':
        return '1011'
    if cond == 'l' or cond == 'nge':
        return '1100'
    if cond == 'nl' or cond == 'ge':
        return '1101'
    if cond == 'le' or cond == 'ng':
        return '1110'
    if cond == 'nle' or cond == 'g':
        return '1111'


def get_sib(base_reg, scale_val, index_reg):
    """corresponds to chart no.8, no.9, and no.10 of slide 09"""
    if scale_val == 1:
        scale = '00'
    elif scale_val == 2:
        scale = '01'
    elif scale_val == 4:
        scale = '10'
    elif scale_val == 8:
        scale = '11'
    else:
        scale = 'error'
    d = {k[2]: v for k, v in registers_dict32.items()}
    if index_reg != 'esp':
        index = d[index_reg]
    else:
        index = 'error'
    base = d[base_reg]
    return scale, index, base


def get_index_only(reg):
    """corresponds to chart no.11 of slide 09"""
    d = {k[2]: v for k, v in registers_dict32.items() if k[2] != 'esp'}
    if reg in d.keys():
        return d['reg']
    return '100'


def main():
    print('Welcome!\nThis is an assembly-to-machine-code converter.\nSimply choose a mode and then write an assembly' +
          'code operation to get its corresponding machine code.\nWe support the following instructions: \'sub\', ' +
          '\'mov\', \'xor\', \'inc\', and \'mul\'')
    while True:
        print('1. x86\n2. x64\n3. quit')
        mode = int(input('Enter the number of your desired action: '))

        if mode == 1:
            mode = 32
        elif mode == 2:
            mode = 64
        elif mode == 3:
            print('Good Bye :D')
            break
        else:
            print('invalid action. Please, try again.')
            continue

        invalid = False
        instructions = input('Enter the instruction and press enter: ')
        instructions = instructions.split(';')
        instructions = [re.split(', |,| |\n|\t', instruction) for instruction in instructions if instruction != '']
        for i in instructions:
            if '' in i:
                i.remove('')
            if len(i) > 3 or len(i) < 2:
                'unsupported or wrong instruction. Please try again.'
                invalid = True
                break
        if invalid:
            continue
        print(instructions)


reg_values = ['000', '001', '010', '011', '100', '101', '110', '111']
registers_dict32 = {('ax', 'al', 'eax'): '000', ('cx', 'cl', 'ecx'): '001', ('dx', 'dl', 'edx'): '010',
                    ('bx', 'bl', 'ebx'): '011', ('sp', 'ah', 'esp'): '100', ('bp', 'ch', 'ebp'): '101',
                    ('si', 'dh', 'esi'): '110', ('di', 'bh', 'edi'): '111'}
registers_dict64 = {'r' + k[0]: '0' + v for k, v in registers_dict32.items()}
for i in range(8, 16):
    registers_dict64['r' + str(i)] = '1' + reg_values[i - 8]
main()
