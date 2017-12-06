"""--- Day 6: Memory Reallocation ---

A debugger program here is having an issue: it is trying to repair a memory
reallocation routine, but it keeps getting stuck in an infinite loop.

In this area, there are sixteen memory banks; each memory bank can hold any
number of blocks. The goal of the reallocation routine is to balance the
blocks between the memory banks.

The reallocation routine operates in cycles. In each cycle, it finds the
memory bank with the most blocks (ties won by the lowest-numbered memory bank)
and redistributes those blocks among the banks. To do this, it removes all of
the blocks from the selected bank, then moves to the next (by index) memory
bank and inserts one of the blocks. It continues doing this until it runs out
of blocks; if it reaches the last memory bank, it wraps around to the first
one.

The debugger would like to know how many redistributions can be done before a
blocks-in-banks configuration is produced that has been seen before.

For example, imagine a scenario with only four memory banks:

    The banks start with 0, 2, 7, and 0 blocks. The third bank has the most
    blocks, so it is chosen for redistribution.

    Starting with the next bank (the fourth bank) and then continuing to the
    first bank, the second bank, and so on, the 7 blocks are spread out over
    the memory banks. The fourth, first, and second banks get two blocks each,
    and the third bank gets one back. The final result looks like this: 2 4 1
    2.

    Next, the second bank is chosen because it contains the most blocks
    (four). Because there are four memory banks, each gets one block. The
    result is: 3 1 2 3.

    Now, there is a tie between the first and fourth memory banks, both of
    which have three blocks. The first bank wins the tie, and its three blocks
    are distributed evenly over the other three banks, leaving it with none: 0
    2 3 4.

    The fourth bank is chosen, and its four blocks are distributed such that
    each of the four banks receives one: 1 3 4 1.

    The third bank is chosen, and the same thing happens: 2 4 1 2.

At this point, we've reached a state we've seen before: 2 4 1 2 was already
seen. The infinite loop is detected after the fifth block redistribution
cycle, and so the answer in this example is 5.

Given the initial block counts in your puzzle input, how many redistribution
cycles must be completed before a configuration is produced that has been seen
before?

Your puzzle answer was 11137.


--- Part Two ---

Out of curiosity, the debugger would also like to know the size of the loop:
starting from a state that has already been seen, how many block
redistribution cycles must be performed before that same state is seen again?

In the example above, 2 4 1 2 is seen again after four cycles, and so the
answer in that example would be 4.

How many cycles are in the infinite loop that arises from the configuration in
your puzzle input?

Your puzzle answer was 1037.

"""


def find_cycles_until_infinite_loop(initial_allocation_str):
    """Given the number of blocks in each memory location, figure out how many
       reallocation cycles it takes before the reallocation enters an infinite
       loop."""


    #create a list to hold the number of blocks currently in each memory
    #location, and a set to hold strings representing every state we've seen
    #before
    current_allocation = map(int, initial_allocation_str.split())
    seen_allocations = set([initial_allocation_str])

    #figure out how many locations we have (should be 16 in this problem)
    num_locations = len(current_allocation)

    #keep track of how many cycles we run through
    num_cycles = 0

    while True:

        #find the location with the most blocks (lower indices break ties)
        max_blocks = max(current_allocation)
        loc_of_max = current_allocation.index(max_blocks)

        #clear out that location
        current_allocation[loc_of_max] = 0

        #redistribute the blocks
        for i in range(1, max_blocks + 1):
            #start in the next location and loop around to the beginning,
            #adding a block at a time
            current_allocation[(loc_of_max + i) % num_locations] += 1

        #update cycle tally
        num_cycles += 1

        #stringify the current allocation so we can check if we've seen it
        #before
        allocation_str = " ".join(map(str, current_allocation))

        #if we have, stop
        if allocation_str in seen_allocations:
            break
        #otherwise, store the new allocation for posterity
        else:
            seen_allocations.add(allocation_str)

    #return the result
    return num_cycles


def find_cycles_in_infinite_loop(initial_allocation_str):
    """Same setup as before, but this time, figure out the length of the
       infinite loop which is created."""

    #create a list to hold the number of blocks currently in each memory
    #location, and a dictionary to hold strings representing every state we've
    #seen before, along with how many cycles it took to get there
    current_allocation = map(int, initial_allocation_str.split())
    seen_allocations = {initial_allocation_str: 0}

    #figure out how many locations we have (should be 16 in this problem)
    num_locations = len(current_allocation)

    #keep track of how many cycles we run through
    num_cycles = 0

    while True:

        #find the location with the most blocks (lower indices break ties)
        max_blocks = max(current_allocation)
        loc_of_max = current_allocation.index(max_blocks)

        #clear out that location
        current_allocation[loc_of_max] = 0

        #redistribute the blocks
        for i in range(1, max_blocks + 1):
            #start in the next location and loop around to the beginning,
            #adding a block at a time
            current_allocation[(loc_of_max + i) % num_locations] += 1

        #update cycle tally
        num_cycles += 1

        #stringify the current allocation so we can check if we've seen it
        #before
        allocation_str = " ".join(map(str, current_allocation))

        #if we have, stop, recording the cycle count corresponding to the
        #already-seen allocation
        if allocation_str in seen_allocations:
            previous_allocation_cycle_count = seen_allocations[allocation_str]
            break
        #otherwise, store the new allocation for posterity
        else:
            seen_allocations[allocation_str] = num_cycles


    #return the result
    return num_cycles - previous_allocation_cycle_count


print find_cycles_until_infinite_loop("0 2 7 0")
print find_cycles_until_infinite_loop("14 0 15 12 11 11 3 5 1 6 8 4 9 1 8 4")

print find_cycles_in_infinite_loop("14 0 15 12 11 11 3 5 1 6 8 4 9 1 8 4")

