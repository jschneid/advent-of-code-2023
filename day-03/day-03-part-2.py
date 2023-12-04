class Part:
    def __init__(self, line_number, substring, start_index):
        self.line_number = line_number
        self.substring = substring
        self.start_index = start_index
    
    def end_index(self):
        return self.start_index + len(self.substring) - 1
    
def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def gear_ratios_sum(lines):
    total = 0
    parts = []

    for line_index in range(len(lines)):
        line = lines[line_index]
        add_parts(line_index, line, parts)

    for line_index in range(len(lines)):
        line = lines[line_index]
        total += gear_ratios_for_line(line_index, line, parts)
        
    return total

def add_parts(line_index, line, parts):
    x = 0
    part = find_part(line_index, line, x)
    while part is not None:
        parts.append(part)
        
        x = part.end_index() + 2
        part = find_part(line_index, line, x)

def find_part(line_index, line, start_x):
    if start_x > len(line) - 1:
        return None
    
    x0 = None
    for x in range(start_x, len(line)):
        if x0 is None:
            if (line[x].isdigit()):
                x0 = x
        else:
            if (not line[x].isdigit()):
                return Part(line_index, line[x0:x], x0)
            
    if not x0 is None:
        return Part(line_index, line[x0:(len(line))], x0)

def gear_ratios_for_line(line_index, line, parts):
    total = 0
    for x in range(len(line)):
        if is_symbol(line[x]):
            total += gear_ratio(line_index, x, parts)
    return total
    
def is_symbol(character):
    if character.isdigit():
        return False
    if character == '.':
        return False
    return True

def gear_ratio(line_index, x, parts):
    adjacent_parts = []
    for part in parts:
        if (part.start_index <= x + 1) and (part.end_index() >= x - 1) and (abs(part.line_number - line_index) <= 1):
            adjacent_parts.append(part)

    if len(adjacent_parts) == 2:
        return int(adjacent_parts[0].substring) * int(adjacent_parts[1].substring)
    
    return 0

lines = read_input_file_lines()
print(gear_ratios_sum(lines))