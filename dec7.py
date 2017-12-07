
class Disc(object):
    """One disc in the recursive stack."""

    def __init__(self, name, weight, kid_names=None, parent_name=None):
        """Kids are all the discs directly on top of this disc, parent is the
           disc directly supporting this disc."""

        self.name = name
        self.weight = weight
        self.kid_names = kid_names or []
        self.parent_name = parent_name


def find_bottom_disc(roll_call_str):
    """Given the disc roll call (each disc announcing its name, weight, and any
       discs it's supporting), figure out which disc is on the bottom."""

    #go through the roll call, adding Disc objects to our collection
    discs = {}
    for line in roll_call_str.split("\n"):
        #each line is either of the form
        #  name (wt)
        #or of the form
        #  name (wt) -> kid1, kid2, etc

        #split the line on spaces
        tokens = line.split()

        #grab the name and weight and use them to create a Disc object
        name = tokens[0]
        weight = tokens[1][1:-1] #slice off parens
        disc = Disc(name, weight)

        #if there's more to the tokens list, it's the disc's kids
        arrow_and_kids = tokens[2:]
        if arrow_and_kids:
            #ditch the arrow, slice the comma off of each kid but the last
            #(which won't have one), then add in the last kid
            kid_names = ([kid[:-1] for kid
                     in arrow_and_kids[1:-1]] +
                    [arrow_and_kids[-1]])
            disc.kid_names = kid_names

        #add the disc to our collection (a dictionary keyed by disc name)
        discs[name] = disc

    #now that we have all the discs, go through setting parent values
    for disc in discs.itervalues():
        #go through each of the current disc's kids and set the current disc
        #as the kid's parent
        for kid_name in disc.kid_names:
            discs[kid_name].parent_name = disc.name

    #now every disc should have a parent except the very bottom disc (the root
    #of the tree)
    for disc in discs.itervalues():
        if not disc.parent_name:
            return disc.name


with open("dec7.txt") as input_file:
    roll_call_str = input_file.read()

    print find_bottom_disc(roll_call_str)
