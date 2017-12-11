def find_knot_hash_product(lengths, rope_length=256):
    """Given a series of twist lengths, find the product of the first two
       numbers in the sequence after all twists have been completed."""

    #create the rope
    rope = range(rope_length)

    current_position = skip_size = 0

    for length in lengths:
        #figure out if the length is going to wrap around from the end of the
        #rope to the beginning
        pinch_end_loc = current_position + length
        if pinch_end_loc >= rope_length:
            #grab the end piece and the beginning piece separately
            pinch_end_loc = pinch_end_loc % rope_length
            end_section = rope[current_position:]
            beginning_section = rope[:pinch_end_loc]
            pinched_section = end_section + beginning_section

            #reverse the pinched section
            rev_pinched_section = pinched_section[::-1]

            #reassign it to the correct locations
            rev_end_section = rev_pinched_section[:len(end_section)]
            rev_beginning_section = rev_pinched_section[len(end_section):]
            rope[current_position:] = rev_end_section
            rope[:pinch_end_loc] = rev_beginning_section

        #no wrapping necessary
        else:
            #grab the section to reverse
            pinched_section = rope[current_position: pinch_end_loc]

            #reverse the pinched section
            rev_pinched_section = pinched_section[::-1]

            #reassign it to the rope array
            rope[current_position: pinch_end_loc] = rev_pinched_section

        #move the current position and increment skip_size
        current_position = (
            (current_position + length + skip_size) % rope_length)
        skip_size += 1

    #now that all the twisting has happened, verify the result by multiplying
    #the first two numbers
    return rope[0] * rope[1]


print find_knot_hash_product([147, 37, 249, 1, 31, 2, 226, 0, 161, 71, 254,
                              243, 183, 255, 30, 70])
