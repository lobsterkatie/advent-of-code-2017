"""--- Day 12: Digital Plumber ---

Walking along the memory banks of the stream, you find a small village that is
experiencing a little confusion: some programs can't communicate with each
other.

Programs in this village communicate using a fixed system of pipes. Messages
are passed between programs using these pipes, but most programs aren't
connected to each other directly. Instead, programs pass messages between each
other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their
intended recipient, and the programs suspect that some pipes are missing. They
would like you to investigate.

You walk through the village and record the ID of each program and the IDs
with which it can communicate directly (your puzzle input). Each program has
one or more programs with which it can communicate, and these pipes are
bidirectional; if 8 says it can communicate with 11, then 11 will say it can
communicate with 8.

You need to figure out how many programs are in the group that contains
program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record
the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5

In this example, the following programs are in the group that contains program
ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which
has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?

Your puzzle answer was 145.


--- Part Two ---

There are more programs than just the ones in the group containing program ID
0. The rest of them have no way of reaching that group, and still might have
no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either
directly or indirectly. The programs you identified just a moment ago are all
part of the same group. Now, they would like you to determine the total number
of groups.

In the example above, there were 2 groups: one consisting of programs
0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?

Your puzzle answer was 207.

"""


def parse_survey_data(data_lines):
    """Given a list of strings representing the survey data, return a list
       whose indices will correspond to program id's and whose values will be
       lists of the programs to which the given program is connected."""

    programs = [None] * len(data_lines)

    for line in data_lines:
        program_id, connections = line.split(" <-> ")
        program_id = int(program_id)
        connections = map(int, connections.split(", "))
        programs[program_id] = set(connections)

    return programs


def find_group(programs, given_program_id):
    """Given a survey of all pipes, and the program_id of the program whose
       group we're intersted in, find all program_ids in that group,
       including the given program itself."""

    #create a set to hold the id's of all programs to which the given program
    #is connected, either directly or indirectly
    group = set()

    #keep track of which programs we've already examined, which which we've
    #yet to examine
    seen = set([given_program_id])
    to_visit = set([given_program_id])

    #as long as we haven't exhausted the group, keep adding connections
    while to_visit:
        #get the next program id and add it to our set of seen programs
        current_program_id = to_visit.pop()
        seen.add(current_program_id)

        #add the current program's connections to the group
        connections = programs[current_program_id]
        group.update(connections)

        #add any connections we haven't already seen to our to_visit set
        to_visit.update(connections - seen)

    #return the group
    return group


def find_number_of_groups(programs):
    """Given the same survey data as above, find the total number of groups."""

    #keep track of which programs we've already assigned to a group, and all
    #groups we've seen
    programs_accounted_for = set()
    groups = []

    #for each program id, if we haven't seen it in a group yet, find its group
    #and add it to our collections
    for program_id in range(len(programs)):

        #if we've already seen it, move on
        if program_id in programs_accounted_for:
            continue

        #otherwise, find its group and add it to the tally
        group = find_group(programs, program_id)
        groups.append(group)
        programs_accounted_for.update(group)

    #return the number of groups
    return len(groups)




with open("dec12.txt") as input_file:
    programs = parse_survey_data(input_file.readlines())
    print len(find_group(programs, 0))
    print find_number_of_groups(programs)
