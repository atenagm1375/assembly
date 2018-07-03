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

        if self.arg_types[1] == 'd':
            self.analyze_data(self.args[1])

        for j in range(2):
            if self.arg_types[j] == 'r':
                rs = get_register_size(self.args[j])
                if self.size != 0 and rs != self.size:
                    raise InstructionError(bad_expression_msg)
                self.size = rs

                if self.arg_types[1] != 'd':
                    self.reg = registersx64[self.args[0]][1:]
                    if self.mode == size[3]:
                        self.rex = self.rex.replace('r', registersx64[self.args[0]][0])
                else:
                    self.reg = opcode[self.operation]['op']
                    self.rm = registersx64[self.args[0]][1:]
                    if self.mode == size[3]:
                        self.rex = self.rex.replace('r', 1)
                        self.rex = self.rex.replace('b', registersx64[self.args[0]][0])

        self.opcode = self.opcode.replace('w', get_w(self.size))
        if self.mode == size[3]:
            self.rex = Rex.replace('w', 1 if self.size == self.mode else 0)

        if has_operand_prefix(self.mode, self.mode, self.size):
            self.operand_prefix = operand_prefix

        return self.address_prefix + self.operand_prefix + self.rex + self.opcode + self.mod + self.reg + self.rm + \
            self.scale + self.index + self.base + self.displacement + self.data

    def analyze_data(self, val):
        if self.mode == size[2]:
            num_of_bits = 32
        else:
            num_of_bits = 40
        if val[:2] == '0x':
            val = val.replace('0x', '')
            if len(val) % 2 != 0:
                val = '0' + val
            val = bin(int(val, 16))[2:].zfill(num_of_bits)
        else:
            val = bin(int(val))[2:].zfill(num_of_bits)
        self.data = ''.join([val[j - 8:j] for j in range(len(val), -1, -8)])
        if num_of_bits == 40 and len(self.data) > num_of_bits:
            self.extra = '0111' + self.data[40:64]
            self.data = self.data[:40]
        else:
            self.data = self.data[:num_of_bits]


class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
