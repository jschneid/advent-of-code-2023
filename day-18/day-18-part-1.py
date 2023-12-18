def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def trench_perimeter_from_lines(lines):
    grid = [['.'] * 2000 for _ in range(2000)]
    x = 1000
    y = 1000

    for line in lines:
        split_line = line.split(' ')
        direction = split_line[0]
        distance = int(split_line[1])
        if direction == 'L':
            for i in range(x, x - distance, -1):
                grid[y][i] = '#'
            x -= distance
        elif direction == 'R':
            for i in range(x, x + distance):
                grid[y][i] = '#'
            x += distance
        elif direction == 'U':
            for i in range(y, y - distance, -1):
                grid[i][x] = '#'
            y -= distance
        elif direction == 'D':
            for i in range(y, y + distance):
                grid[i][x] = '#'
            y += distance

    trim_blank_rows(grid)
    trim_blank_columns(grid)

    return grid

def trim_blank_rows(grid):
    i = 0
    while i < len(grid):
        if grid[i] == ['.'] * len(grid[i]):
            grid.pop(i)
        else:
            i += 1

def trim_blank_columns(grid):
    i = 0
    while i < len(grid[0]):
        if all(row[i] == '.' for row in grid):
            for row in grid:
                row.pop(i)
        else:
            i += 1

def fill_trench_via_raytracing(grid):
    for y in range(1, len(grid) - 1):
        border_start = None
        border_end = None
        borders_seen = 0
        for x in range(0, len(grid[y])):
            if grid[y][x] == '#' and (x == 0 or grid[y][x - 1] == '.' or grid[y][x - 1] == 'x'):
                border_start = x
            elif grid[y][x] == '.' and grid[y][x - 1] == '#' and x > 0:
                border_end = x - 1
                if border_start == border_end:
                    borders_seen += 1
                elif grid[y-1][border_start] == '#' and grid[y+1][border_end] == '#':
                    borders_seen += 1
                elif grid[y+1][border_start] == '#' and grid[y-1][border_end] == '#':
                    borders_seen += 1

            if borders_seen % 2 == 1 and grid[y][x] == '.':
                grid[y][x] = 'x'

def capacity(grid):
    return sum(row.count('#') + row.count('x') for row in grid)

def debug__print_grid(grid):
    for row in grid:
        print(''.join(row)) 

lines = read_input_file_lines()
grid = trench_perimeter_from_lines(lines)

fill_trench_via_raytracing(grid)

print (capacity(grid))