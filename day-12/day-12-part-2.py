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
        total += possible_arrangement_counts(rows[index], damaged_segment_sizes[index], 0, 0, 0)
    return total

def spring_at(row, index):
    if index < 0:
        return None
    return row[index]

def possible_arrangement_counts(row, damaged_segment_sizes, group, amount, index):
    # If we're at a '?' character, split the execution: Call this method again with that
    # character replaced with '#' and with a '.'. Return the combined results.
    if row[index] == '?':
        total = 0
        row_with_next_section_broken = row[:index] + '#' + row[index + 1:]
        total += possible_arrangement_counts(row_with_next_section_broken, damaged_segment_sizes, group, amount, index)
        row_with_next_section_undamaged = row[:index] + '.' + row[index + 1:]
        total += possible_arrangement_counts(row_with_next_section_undamaged, damaged_segment_sizes, group, amount, index)
        return total 
    
    if row[index] == '#':
        amount += 1

        # We're in a section of "#". If there have been too many sections, or if that section is too long, then not a valid permutation.
        if group >= len(damaged_segment_sizes) or amount > damaged_segment_sizes[group]:
            return 0
    else:
        # If we were in a section of "#" and now we've hit a "." (or EOL), we've reached the
        # end of that section. 
        if spring_at(row, index - 1) == '#': 
            # If that section was too short, not a valid permutation.
            if amount < damaged_segment_sizes[group]:
                return 0

            # The section was the right size!
            group += 1
            amount = 0

    # On to the next index.
    index += 1

    if index == len(row):
        # If we were in a section of "#" and now we've hit EOL, we've reached the
        # end of that section. 
        if spring_at(row, index - 1) == '#': 
            # If that section was too short, not a valid permutation.
            if amount < damaged_segment_sizes[group]:
                return 0

            # The section was the right size!
            group += 1
            amount = 0

    # If we've reached the end of the row, and we had found the expected count of '#' groups, 
    # then we've found a valid permutation.    
    if index == len(row):
        if group == len(damaged_segment_sizes):
            return 1
        else:
            # We're at the end, but there were too few '#' groups.
            return 0

    return possible_arrangement_counts(row, damaged_segment_sizes, group, amount, index)

lines = read_input_file_lines()
rows = read_rows(lines)
damaged_segment_sizes = read_damaged_segment_sizes(lines)

rows = unfold_rows(rows)
damaged_segment_sizes = unfold_damaged_segment_sizes(damaged_segment_sizes)

print(sum_of_possible_arrangement_counts(rows, damaged_segment_sizes))