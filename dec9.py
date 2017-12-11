def get_next_group(input_stream, start_pos):
    """Return a group from the input stream, starting at start_pos."""

    #make sure our starting position is valid
    assertion_str = "first character of a group should be {"
    assert input_stream[start_pos] == "{", assertion_str

    #collect characters from the input stream until we find a }
    group_chars = ["{"]
    i = start_pos + 1
    while True:
        #get the character
        char = input_stream[i]

        #if we find a closing squiggly bracket, add it and be done
        if char == "}":
            group_chars.append("}")
            break

        #if we find another group, parse that and add it
        elif char == "{":
            group = get_next_group(input_stream, i)
            group_chars.extend(group)
            i += len(group)

        #if we hit garbage, collect it and add it to the group
        elif char == "<":
            garbage_len = determine_garbage_len(input_stream, i)
            group_chars.extend(input_stream[i: i + garbage_len])
            i += garbage_len

        #otherwise, just keep going
        else:
            group_chars.append(char)
            i += 1

    return "".join(group_chars)


def determine_garbage_len(input_stream, start_pos):
    """Return the number of characters in the garbage sequence beginning at
       start_pos."""

    #make sure our starting position is valid
    assertion_str = "first character of garbage should be <"
    assert input_stream[start_pos] == "<", assertion_str

    #scan through the input stream, collecting garbage until it ends, keeping
    #track of where we are in the input stream
    i = start_pos + 1
    while True:
        #get the current character and increment i
        char = input_stream[i]
        i += 1

        #if it's an exclamation point, skip the next character
        if char == "!":
            i += 1

        #if we find a closing angle bracket, we're done
        elif char == ">":
            break

    #the number of garbage characters is the difference between our current
    #position and our starting position
    return i - start_pos


def find_group_score(input_stream, outer_group_score=1):
    """Compute the score for the given input stream. Within the stream {...} is
       a group, <...> is garbage, and !x means x is "canceled," regardless of
       what x is. The score for a given group is the always one greater than
       the score of its containing group, and scores for all groups in the
       input stream are totaled to find the overall score."""

    #make sure we've been given a single group
    assertion_str = "given input stream is not a single group"
    assert input_stream[0] == "{" and input_stream[-1] == "}", assertion_str

    #collect all groups inside the given group
    groups = []

    #scan through the characters (except for the first and last, as they are
    #already known to be { and })
    #use a while loop rather than a for loop so that characters can be skipped
    i = 1
    while i < (len(input_stream) - 1):

        #get the current character
        char = input_stream[i]

        #figure out if we're about to start a group
        if char == "{":
            #if so, get that group and append it to our collection
            group = get_next_group(input_stream, i)
            groups.append(group)
            spots_to_skip = len(group)

        #if not, we should be about to start some garbage
        elif char == "<":
            garbage_len = determine_garbage_len(input_stream, i)
            spots_to_skip = garbage_len

        #all else *has* failed
        else:
            assert 1 == 0, "Something went wrong!"

        #if we've done everything right, the next character should be a comma
        #(unless we're at the end of the group)
        comma_index = i + spots_to_skip
        assertion_str = ("should either have found a comma after group/garbage"
                         + " or be at end of group")
        assert (input_stream[comma_index] == "," or
                input_stream[comma_index] == "}"), assertion_str

        #move past the comma and keep going
        i = comma_index + 1

    #now that we have the groups, get their score and add it to the containing
    #group's score
    score = outer_group_score
    for group in groups:
        score += find_group_score(group, outer_group_score + 1)

    return score



with open("dec9.txt") as input_file:
    input_stream = input_file.read()
    print find_group_score(input_stream)

