from deocde import *

print('--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--')
print('Welcome!\nThis is an assembly-to-machine-code converter.\nSimply choose a mode and then write an assembly' +
      'code operation to get its corresponding machine code.\nWe support the following instructions: \'sub\', ' +
      '\'add\', \'xor\', \'not\', and \'mul\'')
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
    # instructions = instructions.replace(' + ', '+')
    # instructions = instructions.replace(' +', '+')
    # instructions = instructions.replace('+ ', '+')
    # instructions = instructions.replace(' * ', '*')
    # instructions = instructions.replace(' *', '*')
    # instructions = instructions.replace('* ', '*')
    # instructions = instructions.replace(' ]', ']')
    # instructions = instructions.replace('[ ', '[')
    instructions = instructions.split(';')
    # instructions = [re.split(', |,| |\n|\t', instruction) for instruction in instructions if instruction != '']
    # ans = ''
    for instruction in instructions:
    #     if '' in instruction:
    #         instruction.remove('')
        instruction = instruction.strip()
        if instruction.count(',') >= 2:
            print('>>> Invalid number of arguments! Please try again.')
            break
        # print(instruction)
    #     ans += decode(instruction)
    #     ans += '\n'
        if instruction != '':
            try:
                print(decode(mode, instruction))
            except InstructionError as err:
                print('>>>', err)
                break

    print('...............................................')
