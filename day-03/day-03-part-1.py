class SubstringWithIndex:
    def __init__(self, substring, index):
        self.substring = substring
        self.index = index
    
    def end_index(self):
        return self.index + len(self.substring) - 1

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def preceding_line(lines, line_index):
    if line_index > 0: 
        return lines[line_index - 1] 

def subsequent_line(lines, line_index):
    if line_index < len(lines) - 1:
        return lines[line_index + 1]

def schematic_part_numbers_sum(lines):
    total = 0

    for line_index in range(len(lines)):
        total += line_part_numbers_sum(preceding_line(lines, line_index), lines[line_index], subsequent_line(lines, line_index))

    return total

def line_part_numbers_sum(preceding_line, line, subsequent_line):
    total = 0

    x = 0
    substringWithRange = find_number(line, x)
    while substringWithRange is not None:
        if is_part_number(preceding_line, line, subsequent_line, substringWithRange):
            total += int(substringWithRange.substring)
        
        x = substringWithRange.end_index() + 2
        substringWithRange = find_number(line, x)

    return total

def find_number(line, start_x):
    if start_x > len(line) - 1:
        return None
    
    x0 = None
    for x in range(start_x, len(line)):
        if x0 is None:
            if (line[x].isdigit()):
                x0 = x
        else:
            if (not line[x].isdigit()):
                return SubstringWithIndex(line[x0:x], x0)
            
    if not x0 is None:
        return SubstringWithIndex(line[x0:(len(line))], x0)

def is_part_number(preceding_line, line, subsequent_line, substringWithRange):
    if substringWithRange.index > 0 and is_symbol(line[substringWithRange.index - 1]):
        return True
    if substringWithRange.end_index() < len(line) - 1 and is_symbol(line[substringWithRange.end_index() + 1]):
        return True
    
    if substringWithRange.index == 0:
        x0 = 0
    else:
        x0 = substringWithRange.index - 1
    
    if substringWithRange.end_index() == len(line) - 1:
        x1 = len(line) - 1
    else:
        x1 = substringWithRange.end_index() + 1

    for x in range(x0, x1 + 1):
        if not preceding_line is None:
            if is_symbol(preceding_line[x]):
                return True
        if not subsequent_line is None:
            if is_symbol(subsequent_line[x]):
                return True
        
    return False

def is_symbol(character):
    if character.isdigit():
        return False
    if character == '.':
        return False
    return True

lines = read_input_file_lines()
print(schematic_part_numbers_sum(lines))   