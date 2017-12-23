def parse_second_arg(registers, instruction):
    """Given an instruction, parse the second argument - if it's a number,
       just return it; if it's another register, return that register's value;
       if it doesn't exist, return None.
    """

    #get the second argument
    second_arg = instruction[6:]

    #if it doesn't exist, return None
    if not second_arg:
        return None

    #otherwise, if it's a number, return it
    elif second_arg.isdigit():
        return int(second_arg)

    #it must be a register - return the value there
    else:
        return registers.setdefault(second_arg, 0)


def parse_instruction(registers, instruction):
    """Parse the given instruction, returning the command, target_register,
       and target_value (if any)."""

    #get the command, target register, and second argument (which may be a
    #value, a register whose value we should check, or non-existent)
    if len(instruction) > 5:
        command, target_register, second_arg = instruction.split(" ")
    else:
        command, target_register, second_arg = instruction.split(" ") + [None]

    #handle the second argument
    if not second_arg:
        second_arg_val = None
    elif second_arg.lstrip("-").isdigit():
        second_arg_val = int(second_arg)
    else:
        second_arg_val = registers.setdefault(second_arg, 0)

    #return the results
    return command, target_register, second_arg_val




def determine_first_recovered_freq(instructions):
    """Given instructions, determine what frequency is recovered the first
       time a recovery instruction is run."""

    #start at the top, with no frequency yet played, and with empty registers
    current_instruction_num = 0
    last_played_freq = None
    registers = {}
    #note that all get operations on registers will actually be setdefault's
    #with a default value of 0, so that registers we haven't hear of yet start
    #with a zero value

    #continue as long as we don't fall off either end or until a frequency is
    #recovered
    while 0 <= current_instruction_num < len(instructions):

        #get and parse the current instruction
        instruction = instructions[current_instruction_num]
        print "executing <", instruction, "> on line", current_instruction_num
        command, target_register, target_value = parse_instruction(registers,
                                                                   instruction)

        #if the command is a jump (and the given register > 0), do it and
        #move on
        if command == "jgz":
            target_register_val = registers.setdefault(target_register, 0)
            if target_register_val > 0:
                current_instruction_num += target_value
                continue

        #if it's a recover instruction (that runs), we're done
        elif command == "rcv":
            target_register_val = registers.setdefault(target_register, 0)
            if target_register_val != 0:
                return last_played_freq

        #otherwise, proceed as normal
        elif command == "snd":
            #play a sound with the frequency stored in the target register
            last_played_freq = registers.setdefault(target_register, 0)

        elif command == "set":
            #set the target register equal to the given value
            registers[target_register] = target_value

        elif command == "add":
            #add the given value to the given register
            registers[target_register] = (
                registers.setdefault(target_register, 0) + target_value)

        elif command == "mul":
            #multiply the given register by the given value
            registers[target_register] = (
                registers.setdefault(target_register, 0) * target_value)

        elif command == "mod":
            #mod the given register by the given value
            registers[target_register] = (
                registers.setdefault(target_register, 0) % target_value)

        #move on to the next instruction
        current_instruction_num += 1





with open("dec18.txt") as input_file:
    instructions = [instruction.strip()
                    for instruction in input_file.readlines()]
    print determine_first_recovered_freq(instructions)





