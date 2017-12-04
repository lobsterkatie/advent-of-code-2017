from math import ceil, floor, sqrt

def find_hop_distance(starting_loc_value):
    """Given squares numbered in an expanding counterclockwise spiral,
       determine the number of horizonal + vertical hops it would take to get
       from starting_loc_value back to square 1.

       The path looks like this:

       37  36  35  34  33  32  31
       38  17  16  15  14  13  30
       39  18   5   4   3  12  29
       40  19   6   1   2  11  28
       41  20   7   8   9  10  27
       42  21  22  23  24  25  26
       43  44  45  46  47 --> ...

       """

    #letting the square with value 1 sit on the origin, the spiral forms a
    #box, with the southeast, southwest, northwest, and northeast corners at
    #coordinates (k, -k), (-k, -k), (-k, k), and (k, k), respectively

    #the highest number in each layer of the spiral comes in the southeast
    #corner (at coords (k, -k), where k is the 0-indexed layer number), and its
    #value is the square of the kth odd number (that is to say, the square of
    #2k+1)

    #letting v stand for the value and k for the layer number, we have
    #   v = (2k + 1)^2
    #   sqrt(v) = 2k + 1
    #   sqrt(v) - 1 = 2k
    #   k = (sqrt(v) - 1) / 2

    #of course, this won't always be a whole number; since we're keying each
    #layer by it's *maximum* value, we'll need to take the ceiling of our
    #result to find the layer number

    #another property of the spiral is that each side of the kth layer is
    #2k + 1 wide, meaning the values at the corners are 2k apart

    #so, once we know what layer the given value is in, we can count backwards
    #from the max to find the location of the value


    #compute which layer (0-indexed) the value is in - this will be k
    #if it's in the 0th layer (meaning the starting value is 1), then all of
    #the math is a) unnecessary and b) more than a little suspect, because
    #it'll involve dividing by zero (let's skip blowing up the universe, shall
    #we?)
    if starting_loc_value == 1:
        return 0
    else:
        v = starting_loc_value
        k = ceil((sqrt(v) - 1) / 2)
        print "Value found in layer", int(k)

    #compute the max value for that layer
    layer_max = (2*k + 1)**2
    print "Layer max =", int(layer_max)

    #compute how many jumps of 2k back from the max it takes to reach our value
    #that will tell us how many sides of the square we need to jump back to
    #find our number - options are 0 (stay on bottom side), 1 (left side),
    # 2 (top), and 3 (right side)

    #first, compute how far away our value is from the max
    diff = layer_max - v

    #next, divide that by the number of hops per side to find the number of
    #sides to jump (take the floor to make it a whole number)
    side_jumps = floor(diff / (2*k))

    #if our starting location is on the bottom of the layer...
    if side_jumps == 0:
        #we know the y-coord already - it's -k - so just compute x by figuring
        #out how many spots to the left to hop
        y_coord = -k
        southeast_corner_value = layer_max
        horizontal_dist = southeast_corner_value - v
        x_coord = k - horizontal_dist
        print "Value found on bottom side of layer,", int(horizontal_dist),
        print "spots to the left of", int(southeast_corner_value)

    #if our starting location is on the lefthand side of the layer...
    elif side_jumps == 1:
        #we know the x-coord already - it's -k - so just compute y by figuring
        #out how many spots up to hop
        x_coord = -k
        southwest_corner_value = layer_max - 2*k
        vertical_dist = southwest_corner_value - v
        y_coord = -k + vertical_dist
        print "Value found on left side of layer,", int(vertical_dist),
        print "spots above", int(southwest_corner_value)

    #if our starting location is on the top of the layer...
    elif side_jumps == 2:
        #we know the y-coord already - it's k - so just compute x by figuring
        #out how many spots right to hop
        y_coord = k
        northwest_corner_value = layer_max - 2*(2*k)
        horizontal_dist = northwest_corner_value - v
        x_coord = -k + horizontal_dist
        print "Value found on top side of layer,", int(horizontal_dist),
        print "spots to the right of", int(northwest_corner_value)

    #finally, if our starting location is on the righthand side of the layer...
    elif side_jumps == 3:
        #we already know the x-coord - it's k - so just compute y by figuring
        #out how many spots down to hop
        x_coord = k
        northeast_corner_value = layer_max - 3*(2*k)
        vertical_dist = northeast_corner_value - v
        y_coord = k - vertical_dist
        print "Value found on right side of layer,", int(vertical_dist),
        print "spots below", int(northeast_corner_value)

    else:
        print "OH NO! Something went wrong!!"

    #now that we know the x- and y-coords, finding the number of hops back to
    #the origin is simple
    origin_hops = abs(x_coord) + abs(y_coord)

    print "Value located at ({x}, {y})".format(x=str(int(x_coord)),
                                               y=str(int(y_coord)))
    print "Jumps to the origin = ", int(origin_hops)

    return origin_hops




    ##### other thoughts as I was working ########


    #taking each square as a lattice point, we can assign square 1 to be at
    #the origin (0,0)

    #once we determine the coordinates of any given square, finding the
    #number of horizontal + vertical hops to get back to square 1 is just a
    #matter of adding the absolute value of each of the coordinates

    #observation: starting from square 1, the path went 1 square right and
    #then 1 square up, then 2 squares left and 2 squares down, then 3
    #squares right and 3 squares up, etc, etc

    #as a consequence, the northeast and southwest corners of the path are
    #going to take turns being 2Tn away from 1 in numerical value, where Tn
    #is the nth triangle number, or n(n+1)/2 (the odd n's will end up in the
    #northeast, and the even n's will end up in the southwest)

    #the northwest corner will have a numerical value halfway between the
    #northeast and southwest corners (or 1+ 2Tn + (n+1) for an odd n, or
    #1+ 2Tn - n for an even n), and the southeast corner will be the same
    #distance past the southwest (or 1 + 2Tn + n for an even n)

    #bringing this back to coordinates, that means that the square at (k, k)
    #will have value 1 + 2Tn, where n is the kth odd number greater than zero,
    #or 2k -1

    #substitution gives 1 + 2Tn = 1 + 2(n(n+1)/2) = 1 + n(n+1) =
    #1 + (2k - 1)(2k - 1 + 1) = 1 + (2k - 1)(2k) = 4k^2 - 2k + 1 for the value
    #of the square at (k,k)

    #similarly, the southwest corner at (-k, -k) (which we've seen will have
    #value 1 + 2Tn where n is the kth even number greater than zero, or 2k)
    #will therefore have value 1 + 2Tn = 1 + 2(n(n+1)/2) = 1 + n(n+1) =
    #1 + 2k(2k + 1) = 4k^2 + 2k + 1


    # y = 4k^2 - 2k + 1
    # y - 1 = 4k^2 - 2k
    # (y-1)/4 = k^2-.05k
    # (y-1)/4 +1/16 = k^2-.05k +1/16 = (k-1/4)^2
    # (4y - 4 + 1)/16 = (k-1/4)^2
    # (4y-3)/16 = (k-1/4)^2
    # sqrt(4y-3)/4 = k-1/4
    # k = .25(1+ sqrt(4y-3))







