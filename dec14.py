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


print find_num_used_squares("amgozmfv")



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

