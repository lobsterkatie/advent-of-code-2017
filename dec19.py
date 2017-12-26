"""--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a
routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -,
and +) show the path it needs to take, starting by going down onto the only
line connected to the top of the diagram. It needs to follow this path until
it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to
continue going the same direction, and only turn left or right when there's no
other option. In addition, someone has left letters on the line; these also
don't change its direction, but it can use them to keep track of where it's
been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go
    down, pass through A, and continue onward to the first +.

    Travel right, up, and right, passing through B in the process.

    Continue down (collecting C), right, and up (collecting D).

    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What
letters will it see (in the order it would see them) if it follows the path?
(The routing diagram is very wide; make sure you view it without line
wrapping.)

Your puzzle answer was PVBSCMEQHY.


--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

Your puzzle answer was 17736.

"""


from string import ascii_uppercase


class Packet(object):
    """A lost packet"""

    def __init__(self, path):
        self.path = path


    def find_starting_location(self):
        """Figure out where the path starts (and therefore where the packet
           should start) and set current location and direction."""

        self.current_row = 0
        self.current_col = self.path[0].index("|")
        self.current_direction = "down"


    def make_move(self):
        """Update the current position by moving one hop in the given
           direction."""

        if self.current_direction == "up":
            self.current_row -= 1
        if self.current_direction == "down":
            self.current_row += 1
        if self.current_direction == "left":
            self.current_col -= 1
        if self.current_direction == "right":
            self.current_col += 1


    def _peek(self, direction):
        """Peek one square in the given direction from current location."""

        if direction == "up":
            return self.path[self.current_row - 1][self.current_col]
        if direction == "down":
            return self.path[self.current_row + 1][self.current_col]
        if direction == "left":
            return self.path[self.current_row][self.current_col - 1]
        if direction == "right":
            return self.path[self.current_row][self.current_col + 1]


    def update_direction(self):
        """We've found a + sign, so figure out which direction to turn."""

        #we're turning 90 degrees, so look at directions perpendicular to the
        #current direction of travel
        if self.current_direction in ["up", "down"]:
            for direction in ["left", "right"]:
                if self._peek(direction) == "-":
                    self.current_direction = direction
                    return
            #if we make it here, something went wrong
            print "ack"

        elif self.current_direction in ["left", "right"]:
            for direction in ["up", "down"]:
                if self._peek(direction) == "|":
                    self.current_direction = direction
                    return
            #if we make it here, something went wrong
            print "ack"




def collect_letters(path):
    """Follow the path, collecting letters along the way. Return the letters in
       the order in which they were collected."""

    letters_collected = []

    #create the packet, and start it on its way
    packet = Packet(path)
    packet.find_starting_location()

    #just for interest's sake
    num_steps = 0
    num_direction_changes = 0

    #keep following the path until it runs out
    while True:

        #move in the current direction
        packet.make_move()
        num_steps += 1

        # print "curent location", packet.current_row, packet.current_col,
        # print packet.current_direction

        #decide what to do next based on what we find there
        current_square = path[packet.current_row][packet.current_col]

        #if we find a blank space, we're done
        if current_square == " ":
            break

        #if we find a + sign, change direction
        elif current_square == "+":
            packet.update_direction()
            num_direction_changes += 1
            # print "changing direction to", packet.current_direction

        #if we find a letter, collect it
        elif current_square in ascii_uppercase:
            letters_collected.append(current_square)
            # print "FOUND", current_square

    print "ending location", packet.current_row, packet.current_col
    print num_steps, "steps,", num_direction_changes, "direction changes"

    #now that we've walked the whole path, return the letters in the order
    #they were collected
    return "".join(letters_collected)






with open("dec19.txt") as input_file:
    #read in the lines of the file and find the widest one
    path_lines = input_file.read().split("\n")
    max_width = max(len(line) for line in path_lines)

    #use spaces to right-pad (using spaces) any which are shorter than the max
    path = [line.ljust(max_width) for line in path_lines]

    print collect_letters(path) #17736 steps! (turns out that's part 2)

