"""--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower
of programs that have gotten themselves into a bit of trouble. A recursive
algorithm has gotten out of hand, and now they're balanced precariously in a
large tower.

One program at the bottom supports the entire tower. It's holding a large
disc, and on the disc are balanced several more sub-towers. At the bottom of
these sub-towers, standing on the bottom disc, are other programs, each
holding their own disc, and so on. At the very tops of these sub-sub-
sub-...-towers, many programs stand simply keeping the disc below them
balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these
towers. You ask each program to yell out their name, their weight, and (if
they're holding a disc) the names of the programs immediately above them
balancing on that disc. You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion; by
the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks
like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and
is holding up ugml, padx, and fwft. Those programs are, in turn, holding up
other programs; in this example, none of those programs are holding up any
other programs, and are all the tops of their own towers. (The actual tower
balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is
correct. What is the name of the bottom program?

Your puzzle answer was bsfpjtc.


--- Part Two ---

The programs explain the situation: they can't get down. Rather, they could
get down, if they weren't expending all of their energy trying to keep the
tower balanced. Apparently, one program has the wrong weight, and until it's
fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a
sub-tower. Each of those sub-towers are supposed to be the same weight, or the
disc itself isn't balanced. The weight of a tower is the sum of the weights of
the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo,
ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc
and all programs above it must each match. This means that the following sums
must all be the same:

    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the
other two. Even though the nodes above ugml are balanced, ugml itself is too
heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need
to be to balance the entire tower?

Your puzzle answer was 529.

"""


class Disc(object):
    """One disc in the recursive stack."""

    def __init__(self, name, weight, kids=None, parent=None):
        """Kids are all the discs directly on top of this disc, parent is the
           disc directly supporting this disc."""

        self.name = name
        self.weight = weight
        self.kids = kids or []
        self.parent = parent

    def __repr__(self):
        """Provide useful output when printing."""

        kids = [kid.name for kid in self.kids]
        repr_str = "<Disc {name}  kids: {kids} balanced: {balanced}>"
        return repr_str.format(name=self.name,
                               kids=kids,
                               balanced=self.is_balanced)


def create_disc_tree(roll_call_str):
    """Given the disc roll call (each disc announcing its name, weight, and any
       discs it's supporting), create the disc tree by initializing Disc
       objects and setting their kids and parent values. Returns a dictionary
       of {disc_name: Disc object}."""

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
        weight = int(tokens[1][1:-1]) #slice off parens
        disc = Disc(name, weight)

        #if there's more to the tokens list, it's the disc's kids
        arrow_and_kids = tokens[2:]
        if arrow_and_kids:
            #ditch the arrow, slice the comma off of each kid but the last
            #(which won't have one), then add in the last kid
            kid_names = ([kid[:-1] for kid in arrow_and_kids[1:-1]] +
                         [arrow_and_kids[-1]])
            disc.kids = kid_names

        #add the disc to our collection (a dictionary keyed by disc name)
        discs[name] = disc

    #now that we have all the discs, go through setting parent values
    #also, replace kid names with actual pointers to the kid Disc objects
    for disc in discs.itervalues():
        #temporarily store all the kid Disc objects
        kids = []

        #go through each of the current disc's kids, set the current disc
        #as the kid's parent, and add the kid to our list
        for kid_name in disc.kids:
            kid = discs[kid_name]
            kid.parent = disc
            kids.append(kid)

        #replace kid names with actual kid objects
        disc.kids = kids

    #return the collection of discs
    return discs


def find_bottom_disc(discs):
    """Given a dictionary of {disc_name: Disc object}, figure out which disc is
       on the bottom, and return it."""

    #every disc should have a parent except the very bottom disc (the root
    #of the tree)
    for disc in discs.itervalues():
        if not disc.parent:
            return disc


def calculate_subtree_weights(disc):
    """Given the root of a subtree, calculate the subtree's weight and add it
       as an attribute on the root."""

    #the weight of the subtree is the weight of the root plus the weight of all
    #of its kid subtrees
    disc.subtree_weight = disc.weight
    for kid in disc.kids:
        disc.subtree_weight += calculate_subtree_weights(kid)

    #to make the recursion work, also return the weight of the subtree
    return disc.subtree_weight


def check_balances(disc):
    """Given the root of a subtree, set is_balanced values for each disc in the
       subtree. (A disc is balanced iff all of its subtrees have the same
       weight.)"""

    #first, check the balance of the given disc

    #a subtree rooted at a given disc is balanced iff all of its kids have the
    #same weight
    #if there's more than different weight, the subtree is imbalanced
    kid_weights = [kid.subtree_weight for kid in disc.kids]
    disc.is_balanced = not len(set(kid_weights)) > 1

    #then, recurse down the tree by checking the balance of any kids the disc
    #has
    for kid in disc.kids:
        check_balances(kid)


def find_outlier_subtree(discs):
    """Given a list of discs, each of which is the root of a subtree, such that
       one subtree is a different weight than the rest, return the root of the
       different-weight subtree, along with the weight it should match."""

    #by definition, two different subtree weights are represented here: the
    #odd-one-out's weight, and the everyone-else's weight

    #check the weight of the first subtree against the second and third
    #subtrees - if its weight matches either, that's the everyone-else weight

    #if it matches neither, it's the odd-one-out weight

    #(we need to check it against the second *and* third because if we only
    #checked it against the second, and they didn't match, it wouldn't be
    #clear which one was the outlier)

    if (discs[0].subtree_weight == discs[1].subtree_weight or
        discs[0].subtree_weight == discs[2].subtree_weight):
        everyone_weight = discs[0].subtree_weight

        #now that we know what we're looking for, find the disc with the wrong
        #subtree weight and return it, along with the weight its subtree should
        #be
        for disc in discs:
            if disc.subtree_weight != everyone_weight:
                return disc, everyone_weight

    else: #the first's the outlier
        return discs[0], discs[1].subtree_weight


def find_misweighted_disc(root):
    """Given a dictionary of {disc_name: Disc object} and the name of the disc
       at the bottom of the stack (the root of the tree), figure out which disc
       has the wrong weight and what its weight would need to be to balance the
       tree/stack."""

    #start by calculating the subtree weight for every disc in the tree
    #(this sets a subtree_weight attribute on each disc)
    calculate_subtree_weights(root)

    #once we have the subtree weights, we can figure out which subtrees are
    #balanced (this sets a is_balanced attribute on each disc)
    check_balances(root)

    #by definition, the entire tree is unbalanced, meaning one of the root's
    #kids has a different weight than the rest

    #that kid either is the problem or itself has a kid whose weight is off

    #using the principle, follow the problem down the tree until we find a disc
    #whose subtree weight is different from its siblings' subtree weights but
    #whose kids all have the same weight (in other words, a disc whose parent
    #is imbalanced but who is itself balanced, while having a different subtree
    #weight from its siblings) - that disc is the problem
    current_disc = root
    while not current_disc.is_balanced:

        #if the current disc is imbalanced, one of its kids has the wrong
        #subtree weight; figure out which one, and what the weight *should* be
        problem_child, correct_subtree_weight = (
                                    find_outlier_subtree(current_disc.kids))

        #if our problem child is also imbalanced, keep traversing down the tree
        if not problem_child.is_balanced:
            current_disc = problem_child

        #otherwise, we've found the disc we're looking for - return the weight
        #it ought to be
        else:
            error = correct_subtree_weight - problem_child.subtree_weight
            return problem_child.weight + error

    #if we get here, something went wrong
    print "Drat! Something broke!"



with open("dec7.txt") as input_file:
    roll_call_str = input_file.read()
    discs = create_disc_tree(roll_call_str)
    root = find_bottom_disc(discs)
    print "bottom disc:", root.name
    print "problem child corrent weight:", find_misweighted_disc(root)

