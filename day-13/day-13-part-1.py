def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def find_horizontal_line_reflection(pattern):
    for south_line_index in range(1, len(pattern)):
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
            
def summarize_pattern_notes(patterns):
    total = 0
    for pattern in patterns:
        horizontal_reflection = find_horizontal_line_reflection(pattern)
        if horizontal_reflection is not None:
            total += 100 * horizontal_reflection
            continue
        rotated_pattern = rotate_2d_array(pattern)
        vertical_reflection = find_horizontal_line_reflection(rotated_pattern)
        if vertical_reflection is not None:
            total += vertical_reflection
     
    return total        

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