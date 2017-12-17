class Scanner(object):
    """A firewall scanner"""

    def __init__(self, scanner_range):
        self.range = scanner_range
        self.location = 0
        self.direction = "down"

    def move(self):
        """Move one spot within range."""

        #if we're moving down...
        if self.direction == "down":

            #if there's room to move down, do so
            if self.location < self.range - 1:
                self.location += 1

            #otherwise, turn around
            else:
                self.location -= 1
                self.direction = "up"

        #do the same if we're moving up (but, obviously, in reverse)
        else:

            #if there's room to move up, do so
            if self.location > 0:
                self.location -= 1

            #otherwise, turn around
            else:
                self.location += 1
                self.direction = "down"


def parse_input(filepath):
    """Turn the input file into something useful (specifically, a dictionary of
       Scanner objects, keyed by their depths)."""

    scanners = {}

    with open("dec13.txt") as input_file:
        lines = input_file.readlines()
        for line in lines:
            depth, bot_range = line.split(": ")
            scanners[int(depth)] = Scanner(int(bot_range))

    return scanners


def calculate_severity(scanners):
    """Given scanners (their depth and range), calculate the severity of the
       journey through the firewall."""

    #start the packet just outside the firewall
    packet_location = -1

    #keep track of the journey's total severity (layer depth * range for each
    #layer in which the packet is caught)
    total_severity = 0

    #the journey will take the same number of seconds as there are layers
    for _ in range(max(scanners) + 1):

        #move the packet one layer forward
        packet_location += 1

        #if there is a scanner at the top of the layer the packet just entered,
        #the packet is caught - add to the severity
        scanner = scanners.get(packet_location)
        if scanner and scanner.location == 0:
            total_severity += packet_location * scanners[packet_location].range

        #now move the scanners
        for scanner in scanners.itervalues():
            scanner.move()

    #return the total severity for the journey
    return total_severity




print calculate_severity(parse_input("dec13.txt"))

