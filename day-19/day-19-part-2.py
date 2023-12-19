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

def replace_workflow_id(workflows, old_workflow_id, new_workflow_id):
    for workflow in workflows.values():
        for rule in workflow.rules:
            if rule.destination_workflow_id == old_workflow_id:
                rule.destination_workflow_id = new_workflow_id

def condense_workflows(workflows):
    while True:
        workflows_count = len(workflows)

        workflow_ids_to_delete = set()
        for workflow_id, workflow in workflows.items():
            destination_workflow_ids = set()
            for rule in workflow.rules:
                destination_workflow_ids.add(rule.destination_workflow_id)
            if len(destination_workflow_ids) == 1:
                new_workflow_id = destination_workflow_ids.pop()
                replace_workflow_id(workflows, workflow_id, new_workflow_id)
                workflow_ids_to_delete.add(workflow_id)

        for workflow_id in workflow_ids_to_delete:
            del workflows[workflow_id]

        if len(workflows) == workflows_count:
            break

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
condense_workflows(workflows)

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

# These need to be 0 and not 1 for the calculation to be correct for the lowest portion
# of each range.
x_values.add(0)
m_values.add(0)
a_values.add(0)
s_values.add(0)
x_values.add(4000)
m_values.add(4000)
a_values.add(4000)
s_values.add(4000)
x_values = sorted(x_values)
m_values = sorted(m_values)
a_values = sorted(a_values)
s_values = sorted(s_values)

print(f"x_values: {len(x_values)}")
print(f'iterations: {len(x_values) * len(m_values) * len(a_values) * len(s_values)}')

# TODO: Still too many iterations. 

total_accepted_range_combinations = 0
for x_index in range(1, len(x_values)):
    print (f"Processing x_index: {x_index}")
    x = x_values[x_index]
    previous_x = x_values[x_index - 1]
    for m_index in range(1, len(m_values)):
        m = m_values[m_index]
        previous_m = m_values[m_index - 1]
        for a_index in range(1, len(a_values)):
            a = a_values[a_index]
            previous_a = a_values[a_index - 1]
            for s_index in range(1, len(s_values)):
                s = s_values[s_index]
                previous_s = s_values[s_index - 1]
                machine_part = MachinePart(x, m, a, s)
                if is_accepted(machine_part, workflows):
                    total_accepted_range_combinations += (x - previous_x) * (m - previous_m) * (a - previous_a) * (s - previous_s)
                    
print(total_accepted_range_combinations)

