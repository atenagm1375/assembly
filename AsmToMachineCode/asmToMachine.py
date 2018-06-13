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
