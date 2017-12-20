"""--- Day 13: Packet Scanners ---

You need to cross a vast firewall. The firewall consists of several layers,
each with a security scanner that moves back and forth across the layer. To
succeed, you must not be detected by a scanner.

By studying the firewall briefly, you are able to record (in your puzzle
input) the depth of each layer and the range of the scanning area for the
scanner within it, written as depth: range. Each layer has a thickness of
exactly 1. A layer at depth 0 begins immediately inside the firewall; a layer
at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4

This means that there is a layer immediately inside the firewall (with range
3), a second layer immediately after that (with range 2), a third layer which
begins at depth 4 (with range 4), and a fourth layer which begins at depth 6
(also with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Within each layer, a security scanner moves back and forth within its range.
Each security scanner starts at the top and moves down until it reaches the
bottom, then moves up until it reaches the top, and repeats. A security
scanner takes one picosecond to move one step. Drawing scanners as S, the
first few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Your plan is to hitch a ride on a packet about to move through the firewall.
The packet will travel along the top of each layer, and it moves at one layer
per picosecond. Each picosecond, the packet moves one layer forward (its first
move takes it into layer 0), and then the scanners move one step. If there is
a scanner at the top of the layer as your packet enters it, you are caught.
(If a scanner moves into the top of its layer while you are there, you are not
caught: it doesn't have time to notice you before you leave.) If you were to
do this in the configuration above, marking your current position with
parentheses, your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]


Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

In this situation, you are caught in layers 0 and 6, because your packet
entered the layer when its scanner was at the top when you entered it. You are
not caught in layer 1, since the scanner moved into the top of the layer once
you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by
its range. (Ignore layers in which you do not get caught.) The severity of the
whole trip is the sum of these values. In the example above, the trip severity
is 0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately,
what is the severity of your whole trip?

Your puzzle answer was 1928.


--- Part Two ---

Now, you need to pass through the firewall without being caught - easier said
than done.

You can't control the speed of the packet, but you can delay it any number of
picoseconds. For each picosecond you delay the packet before beginning your
trip, all security scanners move one step. You're not in the firewall during
this time; you don't enter layer 0 until you stop delaying the packet.

In the example above, if you delay 10 picoseconds (picoseconds 0 - 9), you
won't get caught:

State after delaying:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 10:
 0   1   2   3   4   5   6
( ) [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 11:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[S] (S) ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 12:
 0   1   2   3   4   5   6
[S] [S] (.) ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 13:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 14:
 0   1   2   3   4   5   6
[ ] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 15:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... ... [ ] (.) [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 16:
 0   1   2   3   4   5   6
[S] [S] ... ... [ ] ... ( )
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Because all smaller delays would get you caught, the fewest number of
picoseconds you would need to delay to get through safely is 10.

What is the fewest number of picoseconds that you need to delay the packet to
pass through the firewall without being caught?

Your puzzle answer was 3830344.

"""


class Scanner(object):
    """A firewall scanner"""

    def __init__(self, depth, scanner_range):
        self.depth = depth
        self.range = scanner_range
        self.cycle_length = 2 * scanner_range - 2


def find_lcm(nums):
    """Returns the least common multiple of the given numbers"""

    #make a set out of the list to remove duplicates
    num_set = set(nums)

    #find the highest number - the lcm will need to be a multiple of that, into
    #which all other numbers will need to divide
    highest = max(num_set)

    multiple_of_max = 1

    #this is guaranteed to finish, because eventually the lcm candidate will
    #equal the product of all of the nums
    while True:

        lcm_candidate = multiple_of_max * highest

        #if all the given numbers go in evenly, we've got our lcm
        if all(lcm_candidate % num == 0 for num in num_set):
            return lcm_candidate

        #otherwise, try the next multiple of the highest number
        else:
            multiple_of_max += 1


def parse_input(filepath):
    """Turn the input file into something useful (specifically, a dictionary of
       Scanner objects, keyed by their depths)."""

    scanners = []

    #add each scanner, keyed by depth
    with open("dec13.txt") as input_file:
        lines = input_file.readlines()
        for line in lines:
            depth, bot_range = map(int, line.split(": "))
            scanners.append(Scanner(depth, bot_range))

    return scanners


def is_packet_caught(scanner, delay=0):
    """Given a scanner and an optional delay, determine if the packet will be
       caught by the scanner."""

    #the packet will get to the scanner at time delay + depth
    packet_arrival = delay + scanner.depth

    #the scanner will be in spot 0 at multiples of its cycle length, so
    #figure out if the packet's arrival time is one
    return packet_arrival % scanner.cycle_length == 0


def calculate_severity(scanners):
    """Given scanners (their depth and range), calculate the severity of the
       journey through the firewall, assuming no delay."""

    #for each scanner which will catch the packet if it enters the firewall
    #at picosecond 0, add the product of it's depth and range to our tally
    return sum(s.depth * s.range for s in scanners if is_packet_caught(s))


def find_safe_delay(scanners):
    """Given scanners (their depth and range), figure out how long to wait to
       enter the firewall to avoid being caught."""

    #there are only so many possibilities before we begin repeating scenarios
    num_possible_delays = find_lcm([scanner.cycle_length
                                    for scanner in scanners])

    #keep trying different delays until we find one which lets us through the
    #firewall safely
    for delay in range(num_possible_delays):
        print "trying delay of", delay

        if all(not is_packet_caught(scanner, delay) for scanner in scanners):
            return delay

    #if we get to here, there's no way through
    print "no way through"



scanners = parse_input("dec13.txt")
print calculate_severity(scanners)
from datetime import datetime
begin = datetime.now()
print find_safe_delay(scanners)
print datetime.now() - begin
