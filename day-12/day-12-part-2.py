class State:
    def __init__(self, index, group, amount, this_spring, previous_spring):
        self.index = index
        self.group = group
        self.amount = amount
        self.this_spring = this_spring
        self.previous_spring = previous_spring
    
    def __eq__(self, other):
        return self.index == other.index and self.group == other.group and self.amount == other.amount and self.this_spring == other.this_spring and self.previous_spring == other.previous_spring
    
    def __hash__(self):
        return self.index + 100 * self.group + 10000 * self.amount + 1000000 * ord(self.this_spring) + 10000000 * ord(self.previous_spring)

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_rows(lines):
    return [row.split()[0] for row in lines]

def read_damaged_segment_sizes(lines):
    csvs = [row.split()[1].split(',') for row in lines]
    return [[int(size) for size in csv] for csv in csvs]

def unfold_rows(rows):
    result = []
    for row in rows:
        unfolded_row = row
        for _ in range(4):
            unfolded_row += '?' + row
        result.append(unfolded_row)
    return result

def unfold_damaged_segment_sizes(damaged_segment_sizes):
    return [damaged_segment_size * 5 for damaged_segment_size in damaged_segment_sizes]

def sum_of_possible_arrangement_counts(rows, damaged_segment_sizes):
    total = 0
    for index in range(len(rows)):
        print (f"Processing row {index} of {len(rows)-1}...")
        total += possible_arrangement_counts(rows[index], damaged_segment_sizes[index])
    return total

def spring_at(row, index):
    if index < 0 or index >= len(row):
        return '.'
    return row[index]

def add_state(states, state, permutations, initial_permutations):
    if state not in states:
        states.add(state)
        permutations[state] = initial_permutations
    else:
        permutations[state] += initial_permutations

def possible_arrangement_counts(row, damaged_segment_sizes):
    states = set()
    initial_state = State(0, 0, 0, row[0], '.')
    states.add(initial_state)
    permutations = {}
    permutations[initial_state] = 1
    total_permutations = 0 

    while len(states) > 0:
        state = states.pop()

        # EOL
        if state.index == len(row):
            group = state.group

            # Invalid state if the last '#' group was too short.
            if state.previous_spring == '#':
                if state.amount != damaged_segment_sizes[group]:
                    continue
                group += 1

            # Invalid state if there weren't enough '#' groups.
            if group < len(damaged_segment_sizes):
                continue

            total_permutations += permutations[state]
            continue

        if state.this_spring == '?':
            next_state = State(state.index, state.group, state.amount, '.', state.previous_spring)
            add_state(states, next_state, permutations, permutations[state])
            next_state = State(state.index, state.group, state.amount, '#', state.previous_spring)
            add_state(states, next_state, permutations, permutations[state])
            continue

        if state.this_spring == '#':
            amount = state.amount + 1

            # We're in a section of "#". If there have been too many sections, or if that section is too long, then not a valid permutation.
            if state.group >= len(damaged_segment_sizes) or amount > damaged_segment_sizes[state.group]:
                continue

            next_state = State(state.index + 1, state.group, amount, spring_at(row, state.index + 1), state.this_spring)
            add_state(states, next_state, permutations, permutations[state])
        else: # '.'
            # If we were in a section of "#" and now we've hit a ".", we've reached the
            # end of that section. 
            if state.previous_spring == '#':
                # If that section was too short, not a valid permutation.
                if state.amount < damaged_segment_sizes[state.group]:
                    continue

                # The section was the right size!
                next_state = State(state.index + 1, state.group + 1, 0, spring_at(row, state.index + 1), state.this_spring)
                add_state(states, next_state, permutations, permutations[state])
            else:
                next_state = State(state.index + 1, state.group, 0, spring_at(row, state.index + 1), state.this_spring)                
                add_state(states, next_state, permutations, permutations[state])

    return total_permutations

lines = read_input_file_lines()
rows = read_rows(lines)
damaged_segment_sizes = read_damaged_segment_sizes(lines)

rows = unfold_rows(rows)
damaged_segment_sizes = unfold_damaged_segment_sizes(damaged_segment_sizes)

print(sum_of_possible_arrangement_counts(rows, damaged_segment_sizes))