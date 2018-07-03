from tables import *


class Instruction:
    def __init__(self, mode, instr, arg1, arg2):
        self.mode = mode
        self.operation = instr
        self.args = [arg1, arg2]
        self.arg_types = ['r', 'r']
        self.size = 0

        self.address_prefix = ''
        self.operand_prefix = ''
        self.rex = ''
        self.opcode = ''
        self.mod = ''
        self.reg = ''
        self.rm = ''
        self.data = ''
        self.scale = ''
        self.index = ''
        self.base = ''
        self.displacement = ''
        self.extra = ''

    def validate_arguments(self):
        if (self.operation == 'not' or self.operation == 'mul') and self.args[1] is not None:
            raise InstructionError(invalid_num_of_args_msg)
        if not (self.operation == 'not' or self.operation == 'mul') and self.args[1] is None:
            raise InstructionError(invalid_num_of_args_msg)
        if isNumber(self.args[0]):
            raise InstructionError(bad_expression_msg)
        if self.args[0] not in registersx64.keys() and self.args[1] not in registersx64.keys():
            valid = False
            for s in instruction_size_set.keys():
                if s in self.args[0] or (self.args[1] is not None and s in self.args[1]):
                    valid = True
            if not valid:
                raise InstructionError(ambiguous_operand_size_msg)
        for j in range(2):
            if self.args[j] is not None:
                if '[' in self.args[j] and ']' not in self.args[j]:
                    raise InstructionError(bad_expression_msg)
                if '[' in self.args[j]:
                    self.arg_types[j] = 'm'
                    for s in instruction_size_set.keys():
                        if s in self.args[j] and self.args[j].find(s) < self.args[j].find('['):
                            self.size = instruction_size_set[s]
                            self.args[j] = self.args[j].replace(s, ' ')
                            self.args[j] = self.args[j].replace('ptr', ' ')
                    self.args[j] = self.args[j].strip()
                    self.args[j].join(self.args[j].split())
                    if self.args[j][0] != '[' or self.args[j][-1] != ']':
                        raise InstructionError(bad_expression_msg)
                elif isNumber(self.args[j]):
                    self.arg_types[j] = 'd'
                elif self.args[j] not in registersx64.keys():
                    raise InstructionError(bad_expression_msg)

    def translate(self):
        if self.arg_types[0] == 'm' and self.arg_types[1] == 'm':
            raise InstructionError(both_mem_msg)
        self.opcode = opcode[self.operation][self.arg_types[0] + self.arg_types[1]]

        for j in range(2):
            if self.arg_types[j] == 'r':
                rs = get_register_size(self.args[j])
                if self.size != 0 and rs != self.size:
                    raise InstructionError(bad_expression_msg)
                self.size = rs

                if self.arg_types[1] != 'd':
                    if self.reg == '':
                        self.reg = registersx64[self.args[j]][1:]
                        if self.mode == size[3]:
                            self.rex = self.rex.replace('r', registersx64[self.args[j]][0])
                    elif self.arg_types[1] == 'r':
                        self.rm = registersx86[self.args[1]]
                        self.mod = '11'
                        if self.mode == size[3]:
                            self.rex = self.rex.replace('b', registersx64[self.args[1]][0])
                            self.rex = self.rex.replace('x', '0')
                        self.reg, self.rm = self.rm, self.reg
                else:
                    self.reg = opcode[self.operation]['op']
                    self.rm = registersx64[self.args[j]][1:]
                    self.mod = '11'
                    if self.mode == size[3]:
                        self.rex = self.rex.replace('r', '1')
                        self.rex = self.rex.replace('b', registersx64[self.args[j]][0])
            if self.arg_types[j] == 'm':
                mem = self.args[j].replace(' ', '')
                mem = mem.replace('[', '')
                mem = mem.replace(']', '')
                mem = mem.split('+')
                if len(mem) == 1 and mem not in registersx86:
                    self.get_displacement()
                    continue
                print(mem)
                for el in mem:
                    if '*' in el:
                        subel = el.split('*')
                        for sel in subel:
                            if sel in registersx86.keys():
                                self.index = sel
                            else:
                                if sel == '1':
                                    self.scale = '00'
                                elif sel == '2':
                                    self.scale = '01'
                                elif sel == '4':
                                    self.scale = '10'
                                elif sel == '8':
                                    self.scale = '11'
                                else:
                                    raise InstructionError(bad_expression_msg)
                    elif el in registersx86.keys():
                        if self.index == '':
                            self.index = el
                        else:
                            self.base = el
                    elif isNumber(el):
                        self.displacement = el
                    else:
                        raise InstructionError(bad_expression_msg)

                mem_size = get_register_size(self.index)
                if has_address_prefix(self.mode, self.mode, mem_size):
                    self.address_prefix = address_prefix
                self.rm = get_reg_rm(self.mode, self.index, self.base if self.base != '' else None)
                if mem_size == size[1]:
                    self.index, self.base = '', ''
                elif self.rm == '100':
                    if self.mode == size[3]:
                        self.rex = self.rex.replace('x', registersx64[self.index][0])
                        self.rex = self.rex.replace('b', registersx64[self.base][0])
                    self.index, self.base = registersx86[self.index], registersx86[self.base]
                    if self.scale == '':
                        self.scale = '00'
                else:
                    if self.mode == size[3]:
                        self.rex = self.rex.replace('b', registersx64[self.index][0])
                        self.rex = self.rex.replace('x', '0')
                    self.index, self.base = '', ''
                disp_size = self.get_displacement()
                self.mod = get_mod(disp_size, True)

        self.opcode = self.opcode.replace('w', get_w(self.size))
        if self.mode == size[3]:
            self.rex = Rex.replace('w', '1' if self.size == self.mode else '0')

        if has_operand_prefix(self.mode, self.mode, self.size):
            self.operand_prefix = operand_prefix

        if self.arg_types[1] == 'd':
            self.data, self.extra = self.analyze_data(self.args[1])

        return self.address_prefix + self.operand_prefix + self.rex + self.opcode + self.mod + self.reg + self.rm + \
            self.scale + self.index + self.base + self.displacement + self.data

    def analyze_data(self, val, num_of_bits=0):
        d, e = '', ''
        if num_of_bits == 0:
            num_of_bits = self.size
            if num_of_bits == size[3]:
                num_of_bits = 40
        isneg = False
        if val[0] == '-':
            isneg = True
            val = val.replace('-', '')
        if val[:2] == '0x':
            val = val.replace('0x', '')
            if len(val) % 2 != 0:
                val = '0' + val
            if isneg:
                val = '-'
                val = tobin(int(val), num_of_bits)
            else:
                val = bin(int(val, 16))[2:].zfill(num_of_bits)
        else:
            if isneg:
                val = '-' + val
                val = tobin(int(val), num_of_bits)
            else:
                val = bin(int(val))[2:].zfill(num_of_bits)
        d = ''.join([val[j - 8:j] for j in range(len(val), -1, -8)])
        if num_of_bits == 40 and len(d) > num_of_bits:
            e = '0111' + d[40:64]
            d = d[:40]
        else:
            d = d[:num_of_bits]
        return d, e

    def get_displacement(self):
        disp_size = 0
        if self.displacement[:2] == '0x':
            if len(bin(int(self.displacement[2:], 16))[2:]) <= 8:
                disp_size = 8
            else:
                disp_size = 32
        self.displacement, junk = self.analyze_data(self.displacement, disp_size)
        return disp_size


class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
