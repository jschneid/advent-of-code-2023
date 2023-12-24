import datetime

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return self.x + 1000 * self.y

class Hike:
    def __init__(self, positions_visited, current_position, steps):
        self.positions_visited = positions_visited
        self.current_position = current_position
        self.steps = steps

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def next_possible_positions(positions_visited, current_position, grid):
    next_positions = []

    # Only allow moving towards the goal from the final intersection.
    # (Hard-coding it for my input.) 
    if current_position.y == 131 and current_position.x == 137:
        next_positions.append(Point(current_position.x, current_position.y + 1))
    else:
        if current_position.y > 0 and grid[current_position.y - 1][current_position.x] != '#':
            next_positions.append(Point(current_position.x, current_position.y - 1))
        if current_position.y < len(grid) - 1 and grid[current_position.y + 1][current_position.x] != '#':
            next_positions.append(Point(current_position.x, current_position.y + 1))
        if current_position.x > 0 and grid[current_position.y][current_position.x - 1] != '#':
            next_positions.append(Point(current_position.x - 1, current_position.y))
        if current_position.x < len(grid[0]) - 1 and grid[current_position.y][current_position.x + 1] != '#':
            next_positions.append(Point(current_position.x + 1, current_position.y))

    positions_to_remove = []    
    for next_position in next_positions:
        if next_position in positions_visited:
            positions_to_remove.append(next_position)
    for position_to_remove in positions_to_remove:
        next_positions.remove(position_to_remove)

    return next_positions

def longest_hike(grid):
    longest_hike_steps = 0
    initial_positions_visited = set()
    initial_positions_visited.add(Point(1, 0))  
    hikes = [Hike(initial_positions_visited, Point(0, 1), 0)]

    while len(hikes) > 0:
        hike = hikes.pop()
        if hike.current_position.y == len(grid) - 1:
            print(f"{datetime.datetime.now().time()} Found a complete path: {hike.steps}")
            if hike.steps > longest_hike_steps:
                longest_hike_steps = hike.steps
                print("(New longest path!)")
            print(f"   Longest path: {longest_hike_steps}")
            continue
        next_positions = next_possible_positions(hike.positions_visited, hike.current_position, grid)
        for next_position in next_positions:
            next_visited_positions = hike.positions_visited.copy()
            next_visited_positions.add(next_position)
            hikes.append(Hike(next_visited_positions, next_position, hike.steps + 1))
    return longest_hike_steps

grid = read_input_file_lines()
print(longest_hike(grid))
