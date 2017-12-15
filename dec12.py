def find_group_cardinality(survey_data, given_program_id):
    """Given a survey of all pipes, and the program_id of the program whose
       group we're intersted in, find the number of programs in that group,
       including the given program itself."""

    #save the data from the survey in a list whose indices will correspond to
    #program id's and whose values will be lists of the programs to which the
    #given program is connected
    programs = [None] * len(survey_data)
    for line in survey_data:
        program_id, connections = line.split(" <-> ")
        program_id = int(program_id)
        connections = map(int, connections.split(", "))
        programs[program_id] = set(connections)

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

    #return the size of the group
    return len(group)




with open("dec12.txt") as input_file:
    survey_data = input_file.readlines()
    print find_group_cardinality(survey_data, 0)
