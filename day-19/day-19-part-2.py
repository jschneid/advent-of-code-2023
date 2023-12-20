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

class Workflow:
    def __init__(self, line):
        self.id = line.split('{')[0]

        rules_string = line.split('{')[1][0:-1]
        self.rules = []
        for rule_string in rules_string.split(','):
            self.rules.append(Rule(rule_string))

    def next_workflow_id(self, part):
        return None

class PossibilityRanges:
    def __init__(self, min_x, max_x, min_m, max_m, min_a, max_a, min_s, max_s):
        self.min_x = min_x
        self.max_x = max_x
        self.min_m = min_m
        self.max_m = max_m
        self.min_a = min_a
        self.max_a = max_a
        self.min_s = min_s
        self.max_s = max_s

    def possibility_count(self):
        if self.min_x > self.max_x or self.min_m > self.max_m or self.min_a > self.max_a or self.min_s > self.max_s:
            return 0
        return (self.max_x - self.min_x + 1) * (self.max_m - self.min_m + 1) * (self.max_a - self.min_a + 1) * (self.max_s - self.min_s + 1)    

    def clone(self):
        return PossibilityRanges(self.min_x, self.max_x, self.min_m, self.max_m, self.min_a, self.max_a, self.min_s, self.max_s)

    def constrain_by(self, rule):
        if rule.category == 'x':
            if rule.operator == '<':
                if self.max_x >= rule.compare_value:
                    self.max_x = rule.compare_value - 1
            else:
                if self.min_x <= rule.compare_value:
                    self.min_x = rule.compare_value + 1
        elif rule.category == 'm':
            if rule.operator == '<':
                if self.max_m >= rule.compare_value:
                    self.max_m = rule.compare_value - 1
            else:
                if self.min_m <= rule.compare_value:
                    self.min_m = rule.compare_value + 1
        elif rule.category == 'a':
            if rule.operator == '<':
                if self.max_a >= rule.compare_value:
                    self.max_a = rule.compare_value - 1
            else:
                if self.min_a <= rule.compare_value:
                    self.min_a = rule.compare_value + 1
        elif rule.category == 's':
            if rule.operator == '<':
                if self.max_s >= rule.compare_value:
                    self.max_s = rule.compare_value - 1
            else:
                if self.min_s <= rule.compare_value:
                    self.min_s = rule.compare_value + 1

    def constrain_by_failed(self, rule):
        if rule.category == 'x':
            if rule.operator == '<':
                if self.min_x < rule.compare_value:
                    self.min_x = rule.compare_value
            else:
                if self.max_x > rule.compare_value:
                    self.max_x = rule.compare_value
        elif rule.category == 'm':
            if rule.operator == '<':
                if self.min_m < rule.compare_value:
                    self.min_m = rule.compare_value
            else:
                if self.max_m > rule.compare_value:
                    self.max_m = rule.compare_value
        elif rule.category == 'a':
            if rule.operator == '<':
                if self.min_a < rule.compare_value:
                    self.min_a = rule.compare_value
            else:
                if self.max_a > rule.compare_value:
                    self.max_a = rule.compare_value
        elif rule.category == 's':
            if rule.operator == '<':
                if self.min_s < rule.compare_value:
                    self.min_s = rule.compare_value
            else:
                if self.max_s > rule.compare_value:
                    self.max_s = rule.compare_value

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

# Trying to loop though each combination of possible x, m, a, s values would take way too long
# (even after applying various optimizations -- attempts at which can be seen in older commits
# of this file!). Therefore, this alternative approach:
#
# Set up a data structure with the minimum and maximum possible remaining values for each of 
# x, m, a, s. Walk the tree of workflows. Each time we encounter a rule, reduce the corresponding
# min or max value by the rule. For example, if we see the rule "x>10", then if we follow that 
# rule to the next workflow node, we know that the minimum possible value for x is 11.
#
# Similarly, when we _fail_ a rule check, we also need to adjust the data structure. For example,
# if we fail the check in the rule "x>10" and go on to the next rule, then the maximum possible 
# value for x is 10.
#
# We do need to clone the possibility_ranges data structure at each check, so that different paths
# through the tree of workflows don't affect one another.
#
# Finally, when we reach an "A", we can add to our count of total possibilities the product of the 
# remaining ranges of each of the x, m, a, s values.
def possibility_count_at(workflow, possibility_ranges, workflows):
    total_possibilities = 0
    failed_rules = []
    for rule in workflow.rules:
        updated_possibility_ranges = possibility_ranges.clone()
            
        if rule.category != None:
            updated_possibility_ranges.constrain_by(rule)

        for failed_rule in failed_rules:
            updated_possibility_ranges.constrain_by_failed(failed_rule)

        if rule.destination_workflow_id == 'A':
            total_possibilities += updated_possibility_ranges.possibility_count()
        elif rule.destination_workflow_id == 'R':
            total_possibilities += 0
        else:
            total_possibilities += possibility_count_at(workflows[rule.destination_workflow_id], updated_possibility_ranges, workflows)

        failed_rules.append(rule)

    return total_possibilities

lines = read_input_file_lines()
workflows = workflows_from_lines(lines)
possibility_ranges = PossibilityRanges(1, 4000, 1, 4000, 1, 4000, 1, 4000)
print(possibility_count_at(workflows['in'], possibility_ranges, workflows))
