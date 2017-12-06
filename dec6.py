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

