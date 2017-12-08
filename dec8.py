from collections import defaultdict


def find_largest_register_value(instructions):
    """Given a series of instructions for adjusting register values, determine
       the greatest register value after all instructions have been followed.
    """

    #create the registers (since int() = 0, any register which doesn't exist
    #yet will be given an initial value of 0)
    registers = defaultdict(int)

    #run through the instructions, executing each one
    for instruction in instructions:
        #parse the instruction
        instruction_parts = instruction.split()

        #reconstruct the condition and evaluate it
        instruction_parts[-3] = "registers['{reg_name}']".format(
                                    reg_name=instruction_parts[-3])
        condition = " ".join(instruction_parts[-3:])
        should_run = eval(condition)

        #if the rest of the instruction should be executed, do so
        if should_run:
            #figure out which register to change and by how much
            register_to_change = instruction_parts[0]
            value_delta = int(instruction_parts[2])
            if instruction_parts[1] == "dec":
                value_delta *= -1

            #make the change
            registers[register_to_change] += value_delta

    #return the max register value
    return max(registers.itervalues())





with open("dec8.txt") as input_file:
    print find_largest_register_value(input_file.readlines())
