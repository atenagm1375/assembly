import re

from deocde import decode, size

print('--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--')
print('Welcome!\nThis is an assembly-to-machine-code converter.\nSimply choose a mode and then write an assembly' +
      'code operation to get its corresponding machine code.\nWe support the following instructions: \'sub\', ' +
      '\'mov\', \'xor\', \'inc\', and \'mul\'')
print('--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--')
while True:
    print('1. x86\n2. x64\n3. quit')
    try:
        mode = int(input('Enter the number of your desired action: '))
    except ValueError:
        print('>>> invalid action. Please, try again.')
        print('...............................................')
        continue

    if mode == 1:
        mode = size[2]
    elif mode == 2:
        mode = size[3]
    elif mode == 3:
        print('Good Bye :D')
        print('...............................................')
        break
    else:
        print('>>> invalid action. Please, try again.')
        print('...............................................')
        continue

    instructions = input('Enter the instruction and press enter: ').lower()
    instructions = instructions.replace(' + ', '+')
    instructions = instructions.replace(' +', '+')
    instructions = instructions.replace('+ ', '+')
    instructions = instructions.replace(' * ', '*')
    instructions = instructions.replace(' *', '*')
    instructions = instructions.replace('* ', '*')
    instructions = instructions.split(';')
    instructions = [re.split(', |,| |\n|\t', instruction) for instruction in instructions if instruction != '']
    ans = ''
    for instruction in instructions:
        if '' in instruction:
            instruction.remove('')

        ans = decode(instruction)

    print(ans)
    print('...............................................')
