"""--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be
dancing.

There are sixteen programs in total, named a through p. They start by standing
in a line: a stands in position 0, b stands in position 1, and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but
    maintain their order otherwise. (For example, s3 on abcde produces cdeab).

    Exchange, written xA/B, makes the programs at positions A and B swap
    places.

    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do
the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle
input). In what order are the programs standing after their dance?

Your puzzle answer was pkgnhomelfdibjac.


--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your
attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs
perform it again and again: including the first dance, a total of one billion
(1000000000) times.

In the example above, their second dance would begin with the order baedc, and
use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

Your puzzle answer was pogbjfihclkemadn.

"""



def spin(dancers, spin_amount):
    """Given the dancers in their current locations, perform a spin by the
       given amount. Works in place."""

    #grab the end dancers who'll end up in front
    end_dancers = dancers[-spin_amount:]

    #grab the rest, those who get shoved towards the end
    shoved_dancers = dancers[:-spin_amount]

    #put them in the new order (in place)
    dancers[:] = end_dancers + shoved_dancers


def exchange(dancers, spot1, spot2):
    """Swap the dancers in spots 1 and 2. Works in place."""

    dancers[spot1], dancers[spot2] = dancers[spot2], dancers[spot1]


def partner(dancers, dancer1, dancer2):
    """Swap dancer1 with dancer2. Works in place."""

    #find the two dancers
    dancer1_index = dancers.index(dancer1)
    dancer2_index = dancers.index(dancer2)

    #swap them
    exchange(dancers, dancer1_index, dancer2_index)


def dance(dancers, moves):
    """Given a list of dance moves, perform them on the given dancers."""

    #each move is a string of the form s[num], x[num]/[num], or p[char]/[char]
    for move in moves:
        instruction = move[0]

        #if it's a spin
        if instruction == "s":
            #figure out by how much
            spin_amount = int(move[1:])
            #do it
            spin(dancers, spin_amount)

        #if it's an exchange
        elif instruction == "x":
            #figure out which dancers to exchange
            spot1, spot2 = map(int, move[1:].split("/"))
            #do it
            exchange(dancers, spot1, spot2)

        #if it's a partnering
        elif instruction == "p":
            #figure out which dancers to partner
            dancer1, dancer2 = move[1:].split("/")
            #do it
            partner(dancers, dancer1, dancer2)


def dance_a_billion(dancers_str, moves):
    """Given a list of dance moves, dance a billion dances."""

    dancers = list(dancers_str)

    #dance one dance
    dance(dancers, moves)

    #figure out the period of the permutation
    period = 1 #we've already done one round by permuting at all
    while True:

        #if we've come back to the original arrangement, stop
        if "".join(dancers) == dancers_str:
            break

        #otherwise, go another round
        period += 1
        dance(dancers, moves)

    #mod by the period to figure out how many permutations actually need to
    #happen and go that many rounds
    for dance_round in range(1000000000 % period):
        dance(dancers, moves)

    return "".join(dancers)




with open("dec16.txt") as input_file:
    moves = input_file.read().split(",")

    dancers = list("abcdefghijklmnop")
    dance(dancers, moves)
    print "".join(dancers)

    print dance_a_billion("abcdefghijklmnop", moves)



