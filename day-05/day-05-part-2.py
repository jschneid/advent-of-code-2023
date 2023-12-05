class MapEntry:
    def __init__(self, destination_range_start, source_range_start, range_length):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def in_source_range(self, source_index):
        return source_index >= self.source_range_start and source_index < self.source_range_start + self.range_length
    
    def destination_index(self, source_index):
        delta = source_index - self.source_range_start
        return self.destination_range_start + delta
    
    def __str__(self):
        return f"{self.destination_range_start} {self.source_range_start} {self.range_length}"

class Map:
    def __init__(self):
        self.map_entries = []

    def add_map_entry(self, map_entry):
        self.map_entries.append(map_entry)

    def destination_index(self, source_index):
        for map_entry in self.map_entries:
            if map_entry.in_source_range(source_index):
                return map_entry.destination_index(source_index)
        return source_index
    
    def __str__(self):
        result = ""
        for map_entry in self.map_entries:
            result += map_entry.__str__()
            result += "\n"
        return result

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_seeds(lines):
    range_bounds = [int(range_bound) for range_bound in lines[0][7:].split()]
    seed_ranges = [range_bounds[index:index + 2] for index in range(0, len(range_bounds), 2)]
    seeds = []
    for seed_range in seed_ranges:
        for index in range(seed_range[0], seed_range[0] + seed_range[1]):
            seeds.append(index)
    return seeds

def read_maps(lines):
    maps = []

    line_index = 3
    while line_index < len(lines):
        map = Map()
        while line_index < len(lines) and lines[line_index] != '':
            split_line = [int(value) for value in lines[line_index].split()]
            map.add_map_entry(MapEntry(split_line[0], split_line[1], split_line[2]))
            line_index += 1 
        maps.append(map)    
        line_index += 2    
    
    return maps;

def seed_location(seed, maps):
    index = seed
    for map in maps:
        index = map.destination_index(index)
    return index

def closest_seed_location(seed_locations):
    return min(seed_locations)

lines = read_input_file_lines()
seeds = read_seeds(lines)
maps = read_maps(lines)
seed_locations = [seed_location(seed, maps) for seed in seeds]
print (closest_seed_location(seed_locations))

# Do I need to work backwards instead, from each possible location value, back through
# the map, to see if it corresponds to one of the seeds in range?
# I could bail out as soon as I get a hit, since that'll be the lowest!