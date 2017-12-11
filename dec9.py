"""--- Day 9: Stream Processing ---

A large stream blocks your path. According to the locals, it's not safe to
cross the stream at the moment because it's full of garbage. You look down at
the stream; rather than water, you discover that it's a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The
characters represent groups - sequences that begin with { and end with }.
Within a group, there are zero or more other things, separated by commas:
either another group or garbage. Since groups can contain other groups, a }
only closes the most-recently-opened unclosed group - that is, they are
nestable. Your puzzle input represents a single, large group which itself
contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with <
and ends with >. Between those angle brackets, almost any character can
appear, including { and }. Within garbage, < has no special meaning.

In a futile attempt to clean up the garbage, some program has canceled some of
the characters within it using !: inside garbage, any character that comes
after ! should be ignored, including <, >, and even another !.

You don't see any characters that deviate from these rules. Outside garbage,
you only find well-formed groups, and garbage always terminates according to
the rules above.

Here are some self-contained pieces of garbage:

    <>, empty garbage.

    <random characters>, garbage containing random characters.

    <<<<>, because the extra < are ignored.

    <{!>}>, because the first > is canceled.

    <!!>, because the second ! is canceled, allowing the > to terminate the
    garbage.

    <!!!>>, because the second ! and the first > are canceled.

    <{o"i!a,<{i<a>, which ends at the first >.

Here are some examples of whole streams and the number of groups they contain:

    {}, 1 group.

    {{{}}}, 3 groups.

    {{},{}}, also 3 groups.

    {{{},{},{{}}}}, 6 groups.

    {<{},{},{{}}>}, 1 group (which itself contains garbage).

    {<a>,<a>,<a>,<a>}, 1 group.

    {{<a>},{<a>},{<a>},{<a>}}, 5 groups.

    {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are
    canceled).

Your goal is to find the total score for all groups in your input. Each group
is assigned a score which is one more than the score of the group that
immediately contains it. (The outermost group gets a score of 1.)

    {}, score of 1.

    {{{}}}, score of 1 + 2 + 3 = 6.

    {{},{}}, score of 1 + 2 + 2 = 5.

    {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.

    {<a>,<a>,<a>,<a>}, score of 1.

    {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.

    {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.

    {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

What is the total score for all groups in your input?

Your puzzle answer was 11898.


--- Part Two ---

Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the
garbage. The leading and trailing < and > don't count, nor do any canceled
characters or the ! doing the canceling.

    <>, 0 characters.

    <random characters>, 17 characters.

    <<<<>, 3 characters.

    <{!>}>, 2 characters.

    <!!>, 0 characters.

    <!!!>>, 0 characters.

    <{o"i!a,<{i<a>, 10 characters.

How many non-canceled characters are within the garbage in your puzzle input?

Your puzzle answer was 5601.

"""


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
            garbage_len, _ = determine_garbage_len(input_stream, i)
            group_chars.extend(input_stream[i: i + garbage_len])
            i += garbage_len

        #otherwise, just keep going
        else:
            group_chars.append(char)
            i += 1

    return "".join(group_chars)



def determine_garbage_len(input_stream, start_pos):
    """Return the number of characters in the garbage sequence beginning at
       start_pos, as well as the number not counting <, >, !, or anything
       canceled by !."""

    #make sure our starting position is valid
    assertion_str = "first character of garbage should be <"
    assert input_stream[start_pos] == "<", assertion_str

    #scan through the input stream, collecting garbage until it ends, keeping
    #track of where we are in the input stream and how many garbage characters
    #count towards the total
    i = start_pos + 1
    count = 0
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

        #if it's any other character, count it
        else:
            count += 1

    #the number of garbage characters is the difference between our current
    #position and our starting position; return that and the count
    return i - start_pos, count



def find_group_score_and_garbage_count(input_stream, outer_group_score=1):
    """Compute the score for the given input stream. Within the stream {...} is
       a group, <...> is garbage, and !x means x is "canceled," regardless of
       what x is. The score for a given group is the always one greater than
       the score of its containing group, and scores for all groups in the
       input stream are totaled to find the overall score. Also determine the
       total number of garbage characters, not counting <, >, !, or anything
       canceled by !."""

    #make sure we've been given a single group
    assertion_str = "given input stream is not a single group"
    assert input_stream[0] == "{" and input_stream[-1] == "}", assertion_str

    #collect all groups inside the given group, and keep track of garbage
    #characters
    groups = []
    total_garbage_count = 0

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
            garbage_len, garbage_char_count = (
                determine_garbage_len(input_stream, i))
            spots_to_skip = garbage_len
            total_garbage_count += garbage_char_count

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
    #group's score; also, add to our total count of garbage characters
    score = outer_group_score
    for group in groups:
        group_score, group_garbage_count = (
            find_group_score_and_garbage_count(group, outer_group_score + 1))
        score += group_score
        total_garbage_count += group_garbage_count

    return score, total_garbage_count




with open("dec9.txt") as input_file:
    input_stream = input_file.read()
    score, garbage_count = find_group_score_and_garbage_count(input_stream)
    print "score", score
    print "garbage", garbage_count

