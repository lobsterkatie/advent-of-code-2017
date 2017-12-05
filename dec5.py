"""--- Day 5: A Maze of Twisty Trampolines, All Alike ---

An urgent interrupt arrives from the CPU: it's trapped in a maze of jump
instructions, and it would like assistance from any programs with spare cycles
to help find the exit.

The message includes a list of the offsets for each jump. Jumps are relative:
-1 moves to the previous instruction, and 2 skips the next one. Start at the
first instruction in the list. The goal is to follow the jumps until one leads
outside the list.

In addition, these instructions are a little strange; after each jump, the
offset of that instruction increases by 1. So, if you come across an offset of
3, you would move three instructions forward, but change it to a 4 for the
next time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3

Positive jumps ("forward") move downward; negative jumps move upward. For
legibility in this example, these offset values will be written all on one
line, with the current instruction marked in parentheses. The following steps
would be taken before an exit is found:

    (0) 3  0  1  -3  - before we have taken any steps.

    (1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all).
                       Fortunately, the instruction is then incremented to 1.

     2 (3) 0  1  -3  - step forward because of the instruction we just modified.
                       The first instruction is incremented again, now to 2.

     2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.

     2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.

     2  5  0  1  -2  - jump 4 steps forward, escaping the maze.

In this example, the exit is reached in 5 steps.

How many steps does it take to reach the exit?

Your puzzle answer was 336905.


--- Part Two ---

Now, the jumps are even stranger: after each jump, if the offset was three or
more, instead decrease it by 1. Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps, and
the offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?

Your puzzle answer was 21985262.

"""


def count_jumps(jump_str):
    """Given a string representing instruction jumps, figure out how many jumps
       it takes to arrive outside the bounds of the instruction set, given that
       each jump increases by 1 each time it's followed."""

    #turn the given string into a list of jumps
    jumps = [int(jump) for jump in jump_str.split()]

    #start at the beginning
    current_index = 0

    #count how many jumps it takes
    jump_count = 0

    #keep going until we break out of the bounds of the jump list
    while 0 <= current_index < len(jumps):

        #figure out how far we need to jump
        next_jump = jumps[current_index]

        #increment the jump instruction for next time
        jumps[current_index] += 1

        #increase our tally
        jump_count += 1

        #make the jump
        current_index += next_jump

    #once we break out, return the result
    return jump_count


def count_jumps2(jump_str):
    """Given a string representing instruction jumps, figure out how many jumps
       it takes to arrive outside the bounds of the instruction set, given that
       each jump increases or decreases by 1 each time it's followed."""

    #turn the given string into a list of jumps
    jumps = [int(jump) for jump in jump_str.split()]

    #start at the beginning
    current_index = 0

    #count how many jumps it takes
    jump_count = 0

    #keep going until we break out of the bounds of the jump list
    while 0 <= current_index < len(jumps):

        #figure out how far we need to jump
        next_jump = jumps[current_index]

        #increment or decrement the jump instruction for next time
        if next_jump >= 3:
            jumps[current_index] -= 1
        else:
            jumps[current_index] += 1

        #increase our tally
        jump_count += 1

        #make the jump
        current_index += next_jump

    #once we break out, return the result
    return jump_count


with open("dec5.txt") as input_file:
    jump_str = input_file.read()

    print count_jumps(jump_str)
    print count_jumps2(jump_str)
