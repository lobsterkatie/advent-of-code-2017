"""--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a
program comes up to you, clearly in distress. "It's my child process," she
says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can
be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need
to determine the fewest number of steps required to reach him. (A "step" means
to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

Your puzzle answer was 650.


--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

Your puzzle answer was 1465.

"""

#thought: use polar coords - staring hexagon is (0,0), ring around that is
#(1, pi/6), (1, 3pi/6), (1, 5pi/6), (1, 7pi/6), (1, 9pi/6), and (1, 11pi/6)

#other thought: staring hexagon at origin, hexagons in columns like x-coords,
#but y-coords jump by 2's - they're even in the even columns and odd in the
#odd columns

#          ____
#         /    \
#    ____/ 0,2  \____
#   /    \      /    \
#  / -1,1 \____/ 1,1  \
#  \      /    \      /
#   \____/ 0,0  \____/
#   /    \      /    \
#  / -1,-1\____/ 1,-1 \
#  \      /    \      /
#   \____/ 0,-2 \____/
#        \      /
#         \____/


#or, let the x-axis squggle

#          ____        ____
#         /    \      /    \
#    ____/ 0,1  \____/ 2,1  \
#   /    \      /    \      /
#  / -1,1 \____/ 1,1  \____/
#  \      /    \      /    \
#   \____/ 0,0  \____/ 2,0  \
#   /    \      /    \      /
#  / -1,0 \____/ 1,0  \____/
#  \      /    \      /    \
#   \____/ 0,-1 \____/ 2,-1 \
#        \      /    \      /
#         \____/      \____/

#basic plan to find hops home - make it to 0 x or 0 y (whichever can be
#accomplished first) then go from there - (0, y) is y hops away, (x, 0) is x
#hops away


def make_one_hop(current_location, direction):
    """Given the current location and the direction to hop, make the hop.
       Modifies current_location in place."""

    #set the correspondence between hop direction and coordinate change
    #each key is the direction plus the parity of the current x-coord - 0 for
    #even and 1 for odd
    hops_to_coords = {"N0": (0, 1), "N1": (0, 1),
                      "S0": (0, -1), "S1": (0, -1),
                      "NE0": (1, 1), "NE1": (1, 0),
                      "NW0": (-1, 1), "NW1": (-1, 0),
                      "SE0": (1, 0), "SE1": (1, -1),
                      "SW0": (-1, 0), "SW1": (-1, -1)}

    #get the parity of the current x, since it affects the way the hop
    #will change the coordinates
    current_x_parity = str(current_location[0] % 2)

    #make the hop
    x_delta, y_delta = hops_to_coords[direction + current_x_parity]
    current_location[0] += x_delta
    current_location[1] += y_delta


def find_distance_home(current_location):
    """Computes the distance back to the origin without modifying
       current_location."""

    temp_location = current_location[:]

    hops_to_home = 0

    #figure out what quadrant we're in, then head back to the origin until
    #we either hit it or hit the x- or y-axis (one of the coords is zero)
    current_x, current_y = temp_location

    #as long as we're not yet on one of the axes, head towards the origin
    #diagonally
    while current_x != 0 and current_y != 0:

        #figure out which direction to go
        if current_x > 0 and current_y > 0: #QI
            direction = "SW"
        elif current_x < 0 and current_y > 0: #QII
            direction = "SE"
        elif current_x < 0 and current_y < 0: #QIII
            direction = "NE"
        elif current_x > 0 and current_y < 0: #QIV
            direction = "NW"

        #make one jump
        make_one_hop(temp_location, direction)
        hops_to_home += 1
        current_x, current_y = temp_location

    #at this point we should be on at least one of the axes (at least one of
    #the coordinates should be zero) so the quickest path is to head along that
    #axis, meaning the non-zero coordinate is the number of jumps to home
    axis_hops_to_home = temp_location[0] or temp_location[1]
    hops_to_home += abs(axis_hops_to_home)

    #return the answer
    return hops_to_home



def compute_hex_hop_dist(hops):
    """Given a list of hops (either N, S, NE, NW, SE, or SW), determine how far
       the hopper is (in number of hops) from the starting location after all
       hops have been hopped."""

    #starting at the origin, follow the hops
    current_location = [0, 0]
    for hop_direction in hops:
        make_one_hop(current_location, hop_direction)

    #figure out how far we are from home and return the answer
    hops_home = find_distance_home(current_location)
    print current_location, hops_home
    return hops_home


def find_max_hop_distance(hops):
    """Given a list of hops (either N, S, NE, NW, SE, or SW), determine the
       farthest the hopper is (in number of hops) from the starting location.
    """

    #starting at the origin, follow the hops, keeping track of max distance
    #from home
    max_dist = 0
    current_location = [0, 0]
    for hop_direction in hops:
        make_one_hop(current_location, hop_direction)
        dist = find_distance_home(current_location)
        max_dist = max(dist, max_dist)

    return max_dist


with open("dec11.txt") as input_file:
    hops = [hop.upper() for hop in input_file.read().split(",")]
    print compute_hex_hop_dist(hops)
    print find_max_hop_distance(hops)




