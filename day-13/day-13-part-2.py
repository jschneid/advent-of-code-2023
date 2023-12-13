def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def find_horizontal_line_reflection(pattern, solution_to_ignore):
    for south_line_index in range(1, len(pattern)):
        if south_line_index == solution_to_ignore:
            continue
        if is_horizontal_line_reflection_at(pattern, south_line_index):
            return south_line_index
    return None
            
def is_horizontal_line_reflection_at(pattern, south_line_index):
    north_line_index = south_line_index - 1
    for _ in range(north_line_index + 1):
        if south_line_index == len(pattern):
            return True
        
        if pattern[south_line_index] != pattern[north_line_index]:
            return False

        north_line_index -= 1
        south_line_index += 1   
    return True
        
def rotate_2d_array(array):
    return [list(reversed(column)) for column in zip(*array)]

def score_pattern(pattern, score_to_ignore):
    solution_to_ignore = None
    if score_to_ignore is not None and score_to_ignore >= 100:
        solution_to_ignore = score_to_ignore / 100
    horizontal_reflection = find_horizontal_line_reflection(pattern, solution_to_ignore)
    if horizontal_reflection is not None:
        return 100 * horizontal_reflection
    
    solution_to_ignore = score_to_ignore
    rotated_pattern = rotate_2d_array(pattern)
    vertical_reflection = find_horizontal_line_reflection(rotated_pattern, solution_to_ignore)
    return vertical_reflection

def score_smudged_pattern(pattern):
    unsmudged_score = score_pattern(pattern, None)
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            smudged_pattern = apply_smudge_to_pattern(pattern, x, y)
            score = score_pattern(smudged_pattern, unsmudged_score)
            if score is not None and score != unsmudged_score:
                return score

def replace_character_in_string(string, index, character):
    return string[:index] + character + string[index + 1:]

def apply_smudge_to_pattern(pattern, x, y):
    smudged_pattern = pattern.copy()
    if pattern[y][x] == '#':
        smudged_pattern[y] = replace_character_in_string(smudged_pattern[y], x, '.')
    else:
        smudged_pattern[y] = replace_character_in_string(smudged_pattern[y], x, '#')

    return smudged_pattern

def summarize_pattern_notes(patterns):
    return sum(score_smudged_pattern(pattern) for pattern in patterns)

def patterns(lines):
    patterns = []
    pattern = []
    for line in lines:
        if line == '':
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns    
    
lines = read_input_file_lines()
patterns = patterns(lines)
print(summarize_pattern_notes(patterns))