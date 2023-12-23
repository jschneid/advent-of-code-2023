class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return self.x + 1000 * self.y

class Hike:
    def __init__(self, previous_position, current_position, steps):
        self.previous_position = previous_position
        self.current_position = current_position
        self.steps = steps

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def next_possible_positions(previous_position, current_position, grid):
    next_positions = []
    if current_position.y > 0 and grid[current_position.y - 1][current_position.x] in ('.', '^'):
        next_positions.append(Point(current_position.x, current_position.y - 1))
    if current_position.y < len(grid) - 1 and grid[current_position.y + 1][current_position.x] in ('.', 'v'):
        next_positions.append(Point(current_position.x, current_position.y + 1))
    if current_position.x > 0 and grid[current_position.y][current_position.x - 1] in ('.', '<'):
        next_positions.append(Point(current_position.x - 1, current_position.y))
    if current_position.x < len(grid[0]) - 1 and grid[current_position.y][current_position.x + 1] in ('.', '>'):
        next_positions.append(Point(current_position.x + 1, current_position.y))
    if previous_position in next_positions:
        next_positions.remove(previous_position)
    return next_positions

def longest_hike(grid):
    longest_hike_steps = 0
    hikes = [Hike(Point(-1, 1), Point(0, 1), 0)]

    while len(hikes) > 0:
        hike = hikes.pop(0)
        if hike.current_position.y == len(grid) - 1:
            if hike.steps > longest_hike_steps:
                longest_hike_steps = hike.steps
            continue
        for next_position in next_possible_positions(hike.previous_position, hike.current_position, grid):
            hikes.append(Hike(hike.current_position, next_position, hike.steps + 1))
    return longest_hike_steps

grid = read_input_file_lines()
print(longest_hike(grid))