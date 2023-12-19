class MachinePart:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

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

lines = read_input_file_lines()
workflows = workflows_from_lines(lines)

x_values = set()
m_values = set()
a_values = set()
s_values = set()
for workflow in workflows.values():
    for rule in workflow.rules:
        if rule.category == 'x':
            x_values.add(rule.compare_value)
            if rule.operator == '<':
                x_values.add(rule.compare_value - 1)
            else:
                x_values.add(rule.compare_value + 1)
        if rule.category == 'm':
            m_values.add(rule.compare_value)
            if rule.operator == '<':
                m_values.add(rule.compare_value - 1)
            else:
                m_values.add(rule.compare_value + 1)
        if rule.category == 'a':
            a_values.add(rule.compare_value)
            if rule.operator == '<':
                a_values.add(rule.compare_value - 1)
            else:
                a_values.add(rule.compare_value + 1)
        if rule.category == 's':
            s_values.add(rule.compare_value)
            if rule.operator == '<':
                s_values.add(rule.compare_value - 1)
            else:
                s_values.add(rule.compare_value + 1)
x_values = sorted(x_values)
m_values = sorted(m_values)
a_values = sorted(a_values)
s_values = sorted(s_values)

# I guess I can do something like I was able to do yesterday:
# - For each of x, m, a, s: 
# - Create a list of values 0-4000 that, for each rule, just barely pass 
#   each rule, and just barely fail it
# - Run each combination of those values through the rules, and see which ones are accepted
# - Calculate the size of each "range" 
# - The total of those sizes is our answer

print(x_values)

print(f'iterations: {len(x_values) * len(m_values) * len(a_values) * len(s_values)}')

# TODO NEXT: Still way too many iterations. 
# Maybe I can start with the rules with "R" results and work backwards and destroy rules from the 
# list that lead only to "R" results? 
# And/or the same with rules with "A" results?
# Shorten up our list of rules, and therefore our search space?

total_accepted_range_combinations = 0
previous_x = 0
previous_m = 0
previous_a = 0
previous_s = 0
for x in x_values:
    for m in m_values:
        for a in a_values:
            for s in s_values:
                machine_part = MachinePart(x, m, a, s)
                if is_accepted(machine_part, workflows):
                    total_accepted_range_combinations += (x - previous_x) * (m - previous_m) * (a - previous_a) * (s - previous_s)
                previous_s = s
            previous_a = a
        previous_m = m
    previous_x = x
                    
print(total_accepted_range_combinations)

