import re

from tables import *


class Instruction:
    def __init__(self, mode, instr, arg1, arg2):
        self.mode = mode
        self.operation = instr
        self.args = [arg1, arg2]
        self.arg_types = ['r', 'r']
        self.size = 0

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
                    print(self.args[j])
                    if self.args[j][0] != '[' or self.args[j][-1] != ']':
                        print('nooooooo', self.args[j][0], self.args[j][-1], self.args[j])
                        raise InstructionError(bad_expression_msg)
                elif isNumber(self.args[j]):
                    self.arg_types[j] = 'd'
                elif self.args[j] not in registersx64.keys():
                    raise InstructionError(bad_expression_msg)

    def translate(self):
        ans = ''
        if self.arg_types[0] == 'm' and self.arg_types[1] == 'm':
            raise InstructionError(both_mem_msg)
        return ans


class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
