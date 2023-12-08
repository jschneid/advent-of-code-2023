from math import lcm

class NodePair:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_instructions(lines):
    return lines[0]

def read_network(lines):
    network = {}
    for line in lines[2:]:
        start_node = line[0:3]
        left_destination_node = line[7:10]
        right_destination_node = line[12:15]
        network.update({start_node: NodePair(left_destination_node, right_destination_node)})
    return network;

def get_start_nodes(network):
    return [node for node in network.keys() if node[2] == 'A']

def steps_to_reach_nodes_ending_in_Z(nodes, instructions, network):
    instruction_pointer = 0
    steps = 0

    # For my input, the count of steps needed for each "thread" to find a solution 
    # exactly equals the cycle time (in steps) to repeatedly circle back around to 
    # that same solution node.
    #
    # Also (in my input), the path from each start node only ever ends up passing 
    # through one distinct solution node (and no other solution nodes).
    #
    # (I made these observations by running the program for just one of each of the
    # start nodes at a time; and noting the node name and step count for each time
    # a destination node was reached.)

    solution_steps = []

    thread_count = len(nodes)
    while len(solution_steps) < thread_count:
        # If any "thread" has reached a destination, record the number of steps that
        # was taken to get there.
        for node in nodes:
            if (is_node_destination(node)):
                solution_steps.append(steps)

        # Save a bit of processing time by stopping processing for a given "thread" when 
        # that thread has found a destination. (This is feasible due to the observation that
        # (in my input) each thread only ever reaches a single distinct destination node.)
        nodes = [node for node in nodes if not is_node_destination(node)]

        # Advance each "thread" to the next node in its path.
        for node_index in range(len(nodes)):
            nodes[node_index] = next_node(instructions[instruction_pointer], nodes[node_index], network)

        instruction_pointer = increment_instruction_pointer(instruction_pointer, instructions)
        steps += 1

    # Now that we know the count of steps for each start node that were needed to reach 
    # a destination node, plus the observations noted above: We can calculate the time needed 
    # for all of the threads to converge on their destination at the same time by finding 
    # the least common multiple of each of those values.
    return lcm(*solution_steps)

def is_node_destination(node):
    return node[2] == 'Z'

def next_node(instruction, node, network):
    if instruction == 'L':
        return network[node].left
    else:
        return network[node].right

def increment_instruction_pointer(instruction_pointer, instructions):
    return (instruction_pointer + 1) % len(instructions)

lines = read_input_file_lines()
instructions = read_instructions(lines)
network = read_network(lines)
start_nodes = get_start_nodes(network)
print(steps_to_reach_nodes_ending_in_Z(start_nodes, instructions, network))