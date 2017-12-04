"""--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-
dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a
location marked 1 and then counting up while spiraling outward. For example,
the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data
must be carried back to square 1 (the location of the only access port for
this memory system) by programs that can only move up, down, left, or right.
They always take the shortest path: the Manhattan Distance between the
location of the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.

    Data from square 12 is carried 3 steps, such as: down, left, left.

    Data from square 23 is carried only 2 steps: up twice.

    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in
your puzzle input all the way to the access port?

Your puzzle answer was 419.


--- Part Two ---

As a stress test on the system, the programs here clear the grid and then
store the value 1 in square 1. Then, in the same allocation order as shown
above, they store the sum of the values in all adjacent squares, including
diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.

    Square 2 has only one adjacent filled square (with value 1), so it also
    stores 1.

    Square 3 has both of the above squares as neighbors and stores the sum of
    their values, 2.

    Square 4 has all three of the aforementioned squares as neighbors and
    stores the sum of their values, 4.

    Square 5 only has the first and fourth squares as neighbors, so it gets
    the value 5.

Once a square is written, its value does not change. Therefore, the first few
squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle answer was 295229.

"""


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




##### other thoughts as I was working on part 1 ########


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








class Matrix(object):
    """A square matrix of numbers, accessed by coordinates, where the value at
       the physical center of the matrix has (x,y) coords (0,0). (Imagine the
       matrix overlaid on the Cartesian plane, with each value on a lattice
       point."""

    def __init__(self, dist_from_axes):
        """The matrix is initialized as a 2D array full of zeros, where the
           zeros at the corders are dist_from_axes away from the center row or
           column."""
        dimension = 2 * dist_from_axes + 1
        self._matrix = [[0 for x in range(dimension)]
                        for y in range(dimension)]

    def _translate_coords(self, x, y):
        """Given (x,y) coordinates, return the corresponding row and column
           values.

           For example, the (x,y) coords

            -2,2   -1,2   0,2   1,2   2,2
            -2,1   -1,1   0,1   1,1   2,1
            -2,0   -1,0   0,0   1,0   2,0
           -2,-1  -1,-1  0,-1  1,-1  2,-1
           -2,-2  -1,-2  0,-2  1,-2  2,-2

           correspond to the matrix coords

           0,0  0,1  0,2  0,3  0,4
           1,0  1,1  1,2  1,3  1,4
           2,0  2,1  2,2  2,3  2,4
           3,0  3,1  3,2  3,3  3,4
           4,0  4,1  4,2  4,3  4,4

        """

        #figure out the matrix row/col which corresponds to the (x,y) origin
        origin_matrix_coord = len(self._matrix) / 2

        #translate that into matrix row and col numbers
        matrix_row_num = origin_matrix_coord - y
        matrix_col_num = origin_matrix_coord + x

        #return the result
        return (matrix_row_num, matrix_col_num)


    def get_value(self, x, y):
        """Return the value at the given (x,y) coordinates. Raises IndexError
           if the given coordinates are off the edge of the matrix."""

        #figure out the matrix row/col which corresponds to the (x,y) origin
        matrix_row_num, matrix_col_num = self._translate_coords(x, y)

        #if either our row or column numbers are negative, we're off the edge
        #of the matrix; same goes if they're >= the matrix's dimension
        if (matrix_row_num < 0 or matrix_col_num < 0 or
            matrix_row_num >= len(self._matrix) or
            matrix_col_num >= len(self._matrix)):
            raise IndexError

        #if we've made it to here, we're still in bounds, so return the
        #corresponding value
        return self._matrix[matrix_row_num][matrix_col_num]



    def set_value(self, x, y, value):
        """Set the value at coordinates (x,y). Raises IndexError if the given
           coordinates are off the edge of the matrix."""

        #figure out the matrix row/col which corresponds to the (x,y) origin
        matrix_row_num, matrix_col_num = self._translate_coords(x, y)

        #if either our row or column numbers are negative, we're off the edge
        #of the matrix; same goes if they're >= the matrix's dimension
        if (matrix_row_num < 0 or matrix_col_num < 0 or
            matrix_row_num >= len(self._matrix) or
            matrix_col_num >= len(self._matrix)):
            raise IndexError

        #now that we know we're in bounds, set the value
        self._matrix[matrix_row_num][matrix_col_num] = value


    def find_sum_of_ajacent(self, x, y):
        """Given (x,y) coordinates of a value in the matrix, compute the sum of
           the adjacent (including diagonally-adjacent) values."""

        total = 0

        #create a list of all the directions to move to get to adjacent spots
        coord_diffs = [(-1, 1), (0, 1), (1, 1), #spots above
                       (-1, 0), (1, 0), #spots L and R
                       (-1, -1), (0, -1), (1, -1)] #spots below

        #look at each adjacent spot; if we're off the edge of the matrix,
        #move on
        for delta_x, delta_y in coord_diffs:
            try:
                total += self.get_value(x + delta_x, y + delta_y)
            except IndexError:
                continue

        #return the final answer
        return total



def find_first_larger_value(value_to_exceed, matrix_size=10):
    """Assuming the same spiral pattern as above, where each square gets as its
       value the sum of all adjacent (including diagonally adjacent) squares
       which currently have values, find the first value larger than the given
       value.

       For reference, the path looks like this (though the values are not
       these):

       17  16  15  14  13
       18   5   4   3  12
       19   6   1   2  11
       20   7   8   9  10
       21  22  23 --> ...

       which gives rise to the following values:

       147  142  133  122   59
       304    5    4    2   57
       330   10    1    1   54
       351   11   23   25   26
       362  747  806   --> ...

    """

    #to follow the path, go R 1, U 1, L 2, D 2, R 3, U 3, L 4, D 4, etc

    #set up each move and the order in which the directions should be taken
    moves = {"down": (0, -1),
             "right": (1, 0),
             "up": (0, 1),
             "left": (-1, 0)}
    next_directions = {"right": "up",
                       "up": "left",
                       "left": "down",
                       "down": "right"}

    #create a (2 * matrix_size + 1) square Matrix of 0's
    matrix = Matrix(matrix_size)

    #keep track of which spot number we're in
    current_spot_num = 1

    #start at the origin, where the first value will be 1
    current_x = current_y = 0
    matrix.set_value(0, 0, 1)

    #the first move should be to the right, and the first number of jumps
    #before we change direction will be 1 (but we haven't done any yet)
    current_direction = "right"
    num_hops_needed_in_direction = 1
    num_hops_done_in_direction = 0

    #as long as we haven't found a value larger than the given value, keep
    #spiraling around and filling in values
    while True:

        #if we've gone as far in this direction as we need to, change to the
        #next direction and update the number of needed hops if necessary
        if num_hops_done_in_direction == num_hops_needed_in_direction:

            #change direction
            new_direction = next_directions[current_direction]
            current_direction = new_direction

            print "Changing direction to", new_direction

            #update number of needed hops if applicable
            if new_direction in ["left", "right"]:
                num_hops_needed_in_direction += 1

            print "Num hops needed =", num_hops_needed_in_direction

            #also, zero out counter for hops done in current direction
            num_hops_done_in_direction = 0


        #now that we're pointed in the right direction, make one hop...
        delta_x, delta_y = moves[current_direction]
        current_x += delta_x
        current_y += delta_y

        #...then set the correct value
        new_value = matrix.find_sum_of_ajacent(current_x, current_y)
        try:
            matrix.set_value(current_x, current_y, new_value)
        except IndexError: #matrix was too small
            break

        #...and increment the counters
        num_hops_done_in_direction += 1
        current_spot_num += 1

        print "Value {v} set at spot {s} (coords ({x}, {y}))".format(
                v=new_value, s=current_spot_num, x=current_x, y=current_y)

        #if we've found a value bigger than the given value, say so and stop
        if new_value > value_to_exceed:
            print "Given value exceeded - stopping"
            return new_value

    #if we make it to here and haven't found the value, our original matrix
    #was too small
    print "Original matrix too small - try setting the matrix_size parameter",
    print "higher than", matrix_size



