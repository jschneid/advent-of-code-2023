import itertools    

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def galaxies_from_map(map):
    galaxies = []
    for y, line in enumerate(map):
        for x, character in enumerate(line):
            if character == '#':
                galaxies.append(Point(x, y))
    return galaxies

def expand_universe_horizontally(galaxies, x):
    for galaxy in galaxies:
        if galaxy.x > x:
            galaxy.x += 999999

def expand_universe_vertically(galaxies, y):
    for galaxy in galaxies:
        if galaxy.y > y:
            galaxy.y += 999999

def expand_the_universe(galaxies, max_x, max_y):
    for x in range(max_x, -1, -1):
        if all(galaxy.x != x for galaxy in galaxies):
            expand_universe_horizontally(galaxies, x)
    for y in range(max_y, -1, -1):
        if all(galaxy.y != y for galaxy in galaxies):
            expand_universe_vertically(galaxies, y)
        
def galaxy_pairs(galaxies):
    return itertools.combinations(galaxies, 2)

def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def sum_of_manhattan_distances(galaxy_pairs):
    return sum(manhattan_distance(galaxy_pair[0], galaxy_pair[1]) for galaxy_pair in galaxy_pairs)

map = read_input_file_lines()
galaxies = galaxies_from_map(map)
expand_the_universe(galaxies, len(map[0]), len(map))
galaxy_pairs = galaxy_pairs(galaxies)
print(sum_of_manhattan_distances(galaxy_pairs))