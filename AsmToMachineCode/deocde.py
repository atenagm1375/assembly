import re

from Instruction import *


def decode(mode, instr):
    re_line = re.compile(
        r'^(?:\S+\s+)?(?P<instr>add|sub|xor|not|mul)\s+(?P<arg1>([A-Za-z0-9_\[\]+*\-]|\s)+)\s*'
        r'(?:,\s*(?P<arg2>([A-Za-z0-9_\[\]+*\-]|\s)+))?'
    )
    instruction = re_line.search(instr)
    if instruction is None:
        return '>>> Invalid instruction! Please try again.'
    instruction = instruction.groupdict()
    instruction = Instruction(mode, instruction['instr'], instruction['arg1'], instruction['arg2'])
    instruction.validate_arguments()
    ans = instruction.translate()
    ans = ' '.join([ans[i : i + 4] for i in range(0, len(ans), 4)])
    return ans
