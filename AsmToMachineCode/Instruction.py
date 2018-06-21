from tables import *


class Instruction:
    def __init__(self, mode, instr, arg1, arg2):
        self.mode = mode
        self.operation = instr
        self.args = (arg1, arg2)
        self.size = mode

    def validate_arguments(self):
        if (self.operation == 'not' or self.operation == 'mul') and self.args[1] is not None:
            raise InstructionError('Invalid number of arguments! Please try again.')
        if '[' in self.args[0] and '[' in self.args[1]:
            raise InstructionError('Both arguments cannot be a memory! Please try again.')


class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
