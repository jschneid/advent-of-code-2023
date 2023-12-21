def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def next_garden_state(garden):
    next_garden = []
    for y in range(len(garden)):
        next_row = ''
        for x in range(len(garden[y])):
            next_row += next_plot_state(garden, y, x)
        next_garden.append(next_row)
    return next_garden

def next_plot_state(garden, y, x):
    plot = garden[y][x]
    if plot == '#':
        return '#'
    
    if y > 0 and garden[y - 1][x] == 'S':
        return 'S'
    if y < len(garden) - 1 and garden[y + 1][x] == 'S':
        return 'S'
    if x > 0 and garden[y][x - 1] == 'S':
        return 'S'
    if x < len(garden[y]) - 1 and garden[y][x + 1] == 'S':
        return 'S'
    
    return '.'

def possible_destinations(garden):
    destinations = 0
    for y in range(len(garden)):
        for x in range(len(garden[y])):
            if garden[y][x] == 'S':
                destinations += 1
    return destinations 
    
garden = read_input_file_lines()
for _ in range(64):
    garden = next_garden_state(garden)
print(possible_destinations(garden))
