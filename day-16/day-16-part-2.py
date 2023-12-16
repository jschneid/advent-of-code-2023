import sys

class Point:
    def __init__(self, y, x):
        self.y = y  
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x + 1000 * self.y

class Tile:
    beam_directions = None

    def __init__(self):
        self.beam_directions = set()

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def tile_at(tiles, y, x):
    point = Point(y, x)
    if point not in tiles:
        tiles[point] = Tile()
    return tiles[point]

def extend_beam(y, x, beam_direction, contraption_layout, tiles):
    if y < 0 or y >= len(contraption_layout) or x < 0 or x >= len(contraption_layout[0]):
        return

    tile = tile_at(tiles, y, x)
    if beam_direction in tile.beam_directions:
        return    
    tile.beam_directions.add(beam_direction)

    feature = contraption_layout[y][x]
    if beam_direction == "E":
        if feature == '.' or feature == '-':
            extend_beam(y, x + 1, "E", contraption_layout, tiles)
        elif feature == '/':
            extend_beam(y - 1, x, "N", contraption_layout, tiles)
        elif feature == '\\':
            extend_beam(y + 1, x, "S", contraption_layout, tiles)
        elif feature == '|':
            extend_beam(y - 1, x, "N", contraption_layout, tiles)
            extend_beam(y + 1, x, "S", contraption_layout, tiles)
    elif beam_direction == "N":
        if feature == '.' or feature == '|':
            extend_beam(y - 1, x, "N", contraption_layout, tiles)
        elif feature == '/':
            extend_beam(y, x + 1, "E", contraption_layout, tiles)
        elif feature == '\\':
            extend_beam(y, x - 1, "W", contraption_layout, tiles)
        elif feature == '-':
            extend_beam(y, x + 1, "E", contraption_layout, tiles)
            extend_beam(y, x - 1, "W", contraption_layout, tiles)
    elif beam_direction == "W":
        if feature == '.' or feature == '-':
            extend_beam(y, x - 1, "W", contraption_layout, tiles)
        elif feature == '/':
            extend_beam(y + 1, x, "S", contraption_layout, tiles)
        elif feature == '\\':
            extend_beam(y - 1, x, "N", contraption_layout, tiles)
        elif feature == '|':
            extend_beam(y - 1, x, "N", contraption_layout, tiles)
            extend_beam(y + 1, x, "S", contraption_layout, tiles)
    elif beam_direction == "S":
        if feature == '.' or feature == '|':
            extend_beam(y + 1, x, "S", contraption_layout, tiles)
        elif feature == '/':
            extend_beam(y, x - 1, "W", contraption_layout, tiles)
        elif feature == '\\':
            extend_beam(y, x + 1, "E", contraption_layout, tiles)
        elif feature == '-':
            extend_beam(y, x + 1, "E", contraption_layout, tiles)
            extend_beam(y, x - 1, "W", contraption_layout, tiles)

def energized_tile_count(tiles):
    return len(tiles)

def max_possible_energy(contraption_layout):
    max_energy = 0 

    for y in range(len(contraption_layout)):
        tiles = {}
        extend_beam(y, 0, "E", contraption_layout, tiles)
        energy = energized_tile_count(tiles)
        if energy > max_energy:
            max_energy = energy
        
        tiles = {}
        extend_beam(y, len(contraption_layout[0]) - 1, "W", contraption_layout, tiles)
        energy = energized_tile_count(tiles)
        if energy > max_energy:
            max_energy = energy

    for x in range(len(contraption_layout[0])):
        tiles = {}
        extend_beam(0, x, "S", contraption_layout, tiles)
        energy = energized_tile_count(tiles)
        if energy > max_energy:
            max_energy = energy
        
        tiles = {}
        extend_beam(len(contraption_layout) - 1, x, "N", contraption_layout, tiles)
        energy = energized_tile_count(tiles)
        if energy > max_energy:
            max_energy = energy
    
    return max_energy

# Python's default maximum function call stack depth is only 1000! Fortunately, we are able to increase it!
sys.setrecursionlimit(3000)

contraption_layout = read_input_file_lines()
print(max_possible_energy(contraption_layout))