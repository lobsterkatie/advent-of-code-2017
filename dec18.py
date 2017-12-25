"""--- Day 18: Duet ---

You discover a tablet containing some strange assembly code labeled simply
"Duet". Rather than bother the sound card with it, you decide to run the code
yourself. Unfortunately, you don't see any documentation, so you're left to
figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are
each named with a single letter and that can each hold a single integer. You
suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out
what they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.

    set X Y sets register X to the value of Y.

    add X Y increases register X by the value of Y.

    mul X Y sets register X to the result of multiplying the value contained
    in register X by the value of Y.

    mod X Y sets register X to the remainder of dividing the value contained
    in register X by the value of Y (that is, it sets X to the result of X
    modulo Y).

    rcv X recovers the frequency of the last sound played, but only when the
    value of X is not zero. (If it is zero, the command does nothing.)

    jgz X Y jumps with an offset of the value of Y, but only if the value of X
    is greater than zero. (An offset of 2 skips the next instruction, an
    offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a
number. The value of a register is the integer it contains; the value of a
number is that number.

After each jump instruction, the program continues with the instruction to
which the jump jumped. After any other instruction, the program continues with
the next instruction. Continuing (or jumping) off either end of the program
terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then
    set it to itself modulo 5, resulting in a value of 4.

    Then, a sound with frequency 4 (the value of a) is played.

    After that, a is set to 0, causing the subsequent rcv and jgz instructions
    to both be skipped (rcv because a is 0, and jgz because a is not greater
    than 0).

    Finally, a is set to 1, causing the next jgz instruction to activate,
    jumping back two instructions to another jump, which jumps again to the
    rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound
played is 4.

What is the value of the recovered frequency (the value of the most recently
played sound) the first time a rcv instruction is executed with a non-zero
value?

Your puzzle answer was 1187.


--- Part Two ---

As you congratulate yourself for a job well done, you notice that the
documentation has been on the back of the tablet this entire time. While you
actually got most of the instructions correct, there are a few key
differences. This assembly code isn't about sound at all - it's meant to be
run twice at the same time.

Each running copy of the program has its own set of registers and follows the
code independently - in fact, the programs don't even necessarily run at the
same speed. To coordinate, they use the send (snd) and receive (rcv)
instructions:

    snd X sends the value of X to the other program. These values wait in a
    queue until that program is ready to receive them. Each program has its
    own message queue, so a program can never receive a message it sent.

    rcv X receives the next value and stores it in register X. If no values
    are in the queue, the program waits for a value to be sent to it. Programs
    do not continue to the next instruction until they have received a value.
    Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register
p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1,
2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1)
and stores it in a, receives another value (both 2) and stores it in b, and
then each receives the program ID of the other program (program 0 receives 1;
program 1 receives 0) and stores it in c. Each program now sees a different
value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for
either of them, and they reach a deadlock. When this happens, both programs
terminate.

It should be noted that it would be equally valid for the programs to run at
different speeds; for example, program 0 might have sent all three values and
then stopped at the first rcv before program 1 executed even its first
instruction.

Once both of your programs have terminated (regardless of what caused them to
do so), how many times did program 1 send a value?

Your puzzle answer was 5969.

"""

from collections import defaultdict


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
        # print "executing <", instruction, "> on line", current_instruction_num
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


class Program(object):
    """An instance of a duet program as described above."""

    def __init__(self, instructions, program_id):
        self.instructions = instructions
        self.program_id = program_id
        self.registers = defaultdict(int)
        self.registers["p"] = program_id
        self.current_instruction_num = 0
        self.state = "running"
        self.msg_queue = []
        self.interlocutor = None
        self.messages_sent = 0


    def get_arg_value(self, argument):
        """Given an argument, which could either be a value, or a register
           whose value we want, return the value as an int."""

        if argument.lstrip("-").isdigit():
            return int(argument)
        else:
            return self.registers[argument]


    def parse_instruction(self, instruction):
        """Parse the given instruction."""

        #split the instruction into a command and one or two following args
        argv = instruction.split(" ")

        #get the command
        command = argv[0]

        #depending on what it is, handle the arguments differently
        if command in ["set", "add", "mul", "mod"]:
            first_arg = argv[1]
            second_arg = self.get_arg_value(argv[2])
        elif command == "rcv":
            first_arg = argv[1]
            second_arg = None
        elif command == "jgz":
            first_arg = self.get_arg_value(argv[1])
            second_arg = self.get_arg_value(argv[2])
        elif command == "snd":
            first_arg = self.get_arg_value(argv[1])
            second_arg = None

        return command, first_arg, second_arg


    def handle_instruction(self):
        """Execute the next instruction and update the instruction pointer."""

        #if the program has already terminated, do nothing
        if self.state == "terminated":
            return

        #if we're now off the end of the instruction list, terminate
        if (self.current_instruction_num < 0 or
            self.current_instruction_num >= len(self.instructions)):
            self.state = "terminated"
            print "TERMINATING PROGRAM", self.program_id, "(off end)"
            return

        #if not, figure out what to do
        instruction = self.instructions[self.current_instruction_num]
        if self.program_id == 1:
            print "\t\t\t\t\t\t",
        print self.program_id, "executing <", instruction, "> on line",
        print self.current_instruction_num
        command, first_arg, second_arg = self.parse_instruction(instruction)

        #if the command is a jump (and the given register > 0), do it and
        #move on
        if command == "jgz":
            if first_arg > 0:
                self.current_instruction_num += second_arg
                return

        #if it's a receive instruction, check the message queue and store
        #the next value we find (if any; if none, wait)
        elif command == "rcv":
            if self.msg_queue:
                self.registers[first_arg] = self.msg_queue.pop(0)
                self.state = "running"
            else:
                self.state = "waiting"
                return

        #otherwise, proceed as normal
        elif command == "snd":
            #add the target value to the other program's message queue
            assert self.interlocutor
            self.interlocutor.msg_queue.append(first_arg)
            self.messages_sent += 1

        elif command == "set":
            #set the target register equal to the given value
            self.registers[first_arg] = second_arg

        elif command == "add":
            #add the given value to the given register
            self.registers[first_arg] += second_arg

        elif command == "mul":
            #multiply the given register by the given value
            self.registers[first_arg] *= second_arg

        elif command == "mod":
            #mod the given register by the given value
            self.registers[first_arg] %= second_arg

        #move on to the next instruction
        self.current_instruction_num += 1



def determine_num_values_sent(instructions):
    """Figure out how many instructions program 1 sends during the running of
       the instructions."""

    #create both the programs, and tell them to talk to each other
    program0 = Program(instructions, 0)
    program1 = Program(instructions, 1)
    program0.interlocutor = program1
    program1.interlocutor = program0

    #as long as the programs aren't both terminated, keep running instructions
    while program0.state != "terminated" or program1.state != "terminated":

        #run the next instruction
        program0.handle_instruction()
        program1.handle_instruction()

        #if this has left the programs in a deadlocked state, terminate both
        if program0.state == "waiting" and program1.state == "waiting":
            program0.state = program1.state = "terminated"
            print "DEADLOCKED - TERMINATING BOTH PROGRAMS"

    #now that both programs have terminated, return the number of messages
    #program 1 has sent
    return program1.messages_sent





with open("dec18.txt") as input_file:
    instructions = [instruction.strip()
                    for instruction in input_file.readlines()]
    print determine_first_recovered_freq(instructions)
    print determine_num_values_sent(instructions)


#TODO fix part 1 for the fact that snd, rcv, and jgz can have numbers as their
#first args, not just register names


# set, add, mul, mod - first arg always reg name, second could be either
# rcv - arg is always reg name (but we don't know this in part 1 - treat like
# snd)

# snd - arg could be either - needs to end up a value
# jgz - both args could be reg name or value - need to end up values


