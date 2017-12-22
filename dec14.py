"""--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the
situation different, you might sit and watch it for a while, but today, you
just don't have that kind of time. It's soaking up valuable system resources
that are needed elsewhere, and so the only option is to help it finish its
task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is
either free or used. On this disk, the state of the grid is tracked by the
bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row
in the grid; each hash contains 128 bits which correspond to individual grid
squares. Each bit of a hash indicates whether that square is free (0) or used
(1).

The hash inputs are a key string (your puzzle input), a dash, and a number
from 0 to 127 corresponding to the row. For example, if your key string were
flqrgnkx, then the first row would be given by the bits of the knot hash of
flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and
so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal
digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128
bits. To convert to bits, turn each hexadecimal digit to its equivalent binary
value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f
becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal
would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear
as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle answer was 8222.


--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is
a group of used squares that are all adjacent, not including diagonals. Every
used square is in exactly one region: lone used squares form their own
isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with
a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V

Of particular interest is the region marked 8; while it does not appear
contiguous in this small view, all of the squares marked 8 are connected when
considering the whole 128x128 grid. In total, in this example, 1242 regions
are present.

How many regions are present given your key string?

Your puzzle answer was 1086.

"""


from dec10 import Rope, xor


def calculate_binary_knot_hash(input_str):
    """Calculate the binary hash of the input string as detailed above and in
       day 10."""

    #create the rope
    rope = Rope()

    #convert the input string to a sequence of ASCII codes and add the
    #standard suffix values to get the twist lengths
    lengths = [ord(char) for char in input_str] + [17, 31, 73, 47, 23]

    #perform 64 rounds of hashing
    for _ in range(64):
        rope.do_one_hash_round(lengths)

    #xor each group of 16 numbers on our rope to create the dense hash
    sparse_hash = rope.rope
    dense_hash = []
    for block_num in range(16):
        #get the block
        block_start = block_num * 16
        block_end = (block_num + 1) * 16
        block = sparse_hash[block_start:block_end]

        #xor it and add it to the dense hash
        xored_block = reduce(xor, block)
        dense_hash.append(xored_block)

    #convert each number in the dense hash to binary
    bits = []
    for decimal_num in dense_hash:
        binary_str = bin(decimal_num)[2:] #slice off the "0b"
        binary_str = "{num:08}".format(num=int(binary_str)) #0-pad if necessary
        bits.extend(binary_str)

    #create the final hash string and return it
    hash_str = "".join(bits)
    assert len(hash_str) == 128, "hash string is wrong length"
    return hash_str


def find_num_used_squares(key_str):
    """Given a key string, find how many squares in the 128 x 128 grid are
       used."""

    #keep track of the total number of used squares
    used_squares = 0

    #add each row's used squares to the total
    row_generator = ("{key}-{num}".format(key=key_str, num=row_num)
                     for row_num in range(128))
    for row in row_generator:
        row_hash = calculate_binary_knot_hash(row)
        used_squares += row_hash.count("1")

    return used_squares


def explore_region(memory_bank, row_num, square_num):
    """Given a starting location, mark all connected used squares with an X."""

    #if this square isn't used, we don't care - return without doing anything
    #same goes if it's a square we've already seen
    if memory_bank[row_num][square_num] in ["0", "X"]:
        return

    #if it is used (and new to us), mark it with an X so we know we've seen
    #it...
    memory_bank[row_num][square_num] = "X"

    #...and explore around it (using if's to make sure we don't fall off the
    #edges)
    if row_num > 0:
        explore_region(memory_bank, row_num - 1, square_num) #look up
    if square_num > 0:
        explore_region(memory_bank, row_num, square_num - 1) #look left
    if square_num < 127:
        explore_region(memory_bank, row_num, square_num + 1) #look right
    if row_num < 127:
        explore_region(memory_bank, row_num + 1, square_num) #look down


def count_regions(key_str):
    """Given a key string, figure out how many distinct, contiguous regions the
       128 x 128 grid contains."""

    region_count = 0

    #create a 2D array to hold the memory squares, and fill them with data
    memory_bank = []
    row_generator = ("{key}-{num}".format(key=key_str, num=row_num)
                     for row_num in range(128))
    for row in row_generator:
        row_hash = calculate_binary_knot_hash(row)
        memory_bank.append(list(row_hash))

    #walk through the memory bank square by square
    for row_num in range(128):
        for square_num in range(128):

            #if we see a 0, we don't care, and if we see an "X", it means it's
            #a used square which is part of an already-discovered region, so we
            #can ignore that as well

            #if we see a 1, it means we've discovered a new region, so up the
            #count and explore the region
            if memory_bank[row_num][square_num] == "1":
                region_count += 1
                explore_region(memory_bank, row_num, square_num)

    return region_count



print find_num_used_squares("amgozmfv")
print count_regions("amgozmfv")

########## testing part 1 ############

# def translate(hash_str):
#     """For easier eyeballing, convert 1's to #'s and 0's to .'s."""
#     chars = []
#     for char in hash_str:
#         new_char = "#" if char == "1" else "."
#         chars.append(new_char)

#     return "".join(chars)


# print translate(calculate_binary_knot_hash("flqrgnkx-0")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-1")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-2")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-3")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-4")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-5")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-6")[:8])
# print translate(calculate_binary_knot_hash("flqrgnkx-7")[:8])
# print
# print find_num_used_squares("flqrgnkx")
# print count_regions("flqrgnkx")

# for row_num in range(128):
#     print translate(calculate_binary_knot_hash("flqrgnkx-" + str(row_num)))

