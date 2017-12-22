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



with open("dec16.txt") as input_file:
    moves = input_file.read().split(",")
    dancers = list("abcdefghijklmnop")
    dance(dancers, moves)
    print "".join(dancers)

