class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'(x={self.x}, y={self.y})'
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def start_position(lines):
    for line_index, line in enumerate(lines):
        start_x = line.find('S')
        if start_x >= 0:
            return Point(start_x, line_index)

def tile_at(lines, point):
    if point.x < 0 or point.x > len(lines[0]) - 1 or point.y < 0 or point.y > len(lines) - 1:
        return '.'
    return lines[point.y][point.x]

def point_east_of(point):
    return Point(point.x + 1, point.y)

def point_south_of(point):
    return Point(point.x, point.y + 1)

def point_west_of(point):
    return Point(point.x - 1, point.y)

def point_north_of(point):
    return Point(point.x, point.y - 1)

def next_point_from_start_point(lines, start_point):
    # Assuming that the start point isn't on an edge
    point_to_the_east = point_east_of(start_point)

    if tile_at(lines, point_to_the_east) in { '-', 'J', '7' }:
        return point_to_the_east
    point_to_the_south = point_south_of(start_point)
    if tile_at(lines, point_to_the_south) in { '|', 'L', 'J' }:
        return point_to_the_south
    return point_west_of(start_point)
    
def next_point_from_point(lines, point, previous_point):
    if previous_point.x < point.x:
        if tile_at(lines, point) == 'J': return point_north_of(point)
        if tile_at(lines, point) == '-': return point_east_of(point)
        return point_south_of(point)
    if previous_point.y < point.y:
        if tile_at(lines, point) == 'J': return point_west_of(point)
        if tile_at(lines, point) == '|': return point_south_of(point)
        return point_east_of(point)
    if previous_point.x > point.x:
        if tile_at(lines, point) == 'L': return point_north_of(point)
        if tile_at(lines, point) == '-': return point_west_of(point)
        return point_south_of(point)
    # previous_point.y > point.y
    if tile_at(lines, point) == 'F': return point_east_of(point)
    if tile_at(lines, point) == '|': return point_north_of(point)
    return point_west_of(point)

def steps_to_tile_in_loop_farthest_from_start(lines):
    start_point = start_position(lines)

    current_point = next_point_from_start_point(lines, start_point)
    previous_point = start_point
    steps = 1
    while current_point != start_point:        
        next_point = next_point_from_point(lines, current_point, previous_point)
        steps += 1
        previous_point = current_point
        current_point = next_point
    return steps / 2
    
lines = read_input_file_lines()
print(steps_to_tile_in_loop_farthest_from_start(lines))