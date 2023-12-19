class MachinePart:
    def __init__(self, line):
        split_line = line[1:-1].split(',')
        self.x = int(split_line[0].split('=')[1])
        self.m = int(split_line[1].split('=')[1])
        self.a = int(split_line[2].split('=')[1])
        self.s = int(split_line[3].split('=')[1])

    def rating(self):
        return self.x + self.m + self.a + self.s

class Rule:
    def __init__(self, rule_string):
        split_rule_string = rule_string.split(':')
        if len(split_rule_string) == 2:
            self.category = split_rule_string[0][0]
            self.operator = split_rule_string[0][1]
            self.compare_value = int(split_rule_string[0][2:])   
            self.destination_workflow_id = split_rule_string[1]
        else:
            self.category = None
            self.operator = None
            self.compare_value = None
            self.destination_workflow_id = rule_string

    def apply_to(self, machine_part):
        if self.category == None:
            return self.destination_workflow_id
        elif self.category == 'x':
            part_value = machine_part.x
        elif self.category == 'm':
            part_value = machine_part.m
        elif self.category == 'a':
            part_value = machine_part.a
        elif self.category == 's':
            part_value = machine_part.s
        
        if self.operator == '<':
            if part_value < self.compare_value:
                return self.destination_workflow_id
        elif self.operator == '>':
            if part_value > self.compare_value:
                return self.destination_workflow_id
        return None

class Workflow:
    def __init__(self, line):
        self.id = line.split('{')[0]

        rules_string = line.split('{')[1][0:-1]
        self.rules = []
        for rule_string in rules_string.split(','):
            self.rules.append(Rule(rule_string))

    def next_workflow_id(self, part):
        return None

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def workflows_from_lines(lines):
    workflows = {}
    for line in lines:
        if line == '':
            return workflows
        add_workflow_from_line(workflows, line)

def add_workflow_from_line(workflows, line):
    workflow = Workflow(line)
    workflows[workflow.id] = workflow    
    return

def machine_parts_from_lines(lines):
    machine_parts = []
    for line in lines:
        if not line.startswith('{'):
            continue
        machine_parts.append(MachinePart(line))
    return machine_parts

def next_workflow_id(workflow, part):
    for rule in workflow.rules:
        next_workflow_id = rule.apply_to(part)
        if next_workflow_id != None:
            return next_workflow_id

def is_accepted(part, workflows):
    workflow_id = 'in'
    while workflow_id not in {'A', 'R'}:
        workflow_id = next_workflow_id(workflows[workflow_id], part)
    return workflow_id == 'A'

def total_accepted_parts_rating(machine_parts, workflows):
    total = 0 
    for part in machine_parts: 
        if is_accepted(part, workflows):
            total += part.rating()
    return total 

lines = read_input_file_lines()
workflows = workflows_from_lines(lines)
machine_parts = machine_parts_from_lines(lines)
print(total_accepted_parts_rating(machine_parts, workflows))
