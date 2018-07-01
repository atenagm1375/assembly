import re

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
        ans = ''
        if self.arg_types[0] == 'm' and self.arg_types[1] == 'm':
            raise InstructionError(both_mem_msg)
        self.opcode = opcode[self.operation][self.arg_types[0] + self.arg_types[1]]
        if self.mode == size[3]:
            self.rex = Rex
        if self.arg_types[1] == 'd':
            self.analyze_data(self.args[1])
        return ans

    def analyze_data(self, val):
        if self.mode == size[2]:
            d = ['0'] * 32
        else:
            d = ['0'] * 40
            self.extra = '0111' + '{0:24b}'.format(0)
        if val[:2] == '0x':
            val = val.replace('0x', '')
            print(val)
            if len(val) % 2 != 0:
                val = '0' + val
                print(val)
            # d = list(self.data)
            for i in range(len(val) - 1, -1, -2):
                d[len(val) - i - 1] = '{0:04b}'.format(int(val[i - 1]))
                d[len(val) - i] = '{0:04b}'.format(int(val[i]))
            self.data = ''.join(d)
            print(self.data)
        else:
            bin(int(val))


class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
