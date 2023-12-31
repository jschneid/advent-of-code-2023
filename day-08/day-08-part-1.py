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

def steps_to_reach_ZZZ(instructions, network):
    instruction_pointer = 0
    node = 'AAA'
    steps = 0
    while node != 'ZZZ':
        steps += 1
        node = next_node(instructions[instruction_pointer], node, network)
        instruction_pointer = increment_instruction_pointer(instruction_pointer, instructions)
    return steps

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
print(steps_to_reach_ZZZ(instructions, network))
