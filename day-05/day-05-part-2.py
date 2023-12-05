class MapEntry:
    def __init__(self, destination_range_start, source_range_start, range_length):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def in_destination_range(self, destination_index):
        return destination_index >= self.destination_range_start and destination_index < self.destination_range_start + self.range_length
    
    def source_index(self, destination_index):
        delta = destination_index - self.destination_range_start
        return self.source_range_start + delta
    
class Map:
    def __init__(self):
        self.map_entries = []

    def add_map_entry(self, map_entry):
        self.map_entries.append(map_entry)

    def source_index(self, destination_index):
        for map_entry in self.map_entries:
            if map_entry.in_destination_range(destination_index):
                return map_entry.source_index(destination_index)
        return destination_index

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_seed_ranges(lines):
    range_bounds = [int(range_bound) for range_bound in lines[0][7:].split()]
    return [range_bounds[index:index + 2] for index in range(0, len(range_bounds), 2)]

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

def seed_for_location(location, maps):
    index = location
    for map in reversed(maps):
        index = map.source_index(index)
    return index

def is_in_range(seed, seed_ranges):
    for seed_range in seed_ranges:
        if seed >= seed_range[0] and seed < seed_range[0] + seed_range[1]:
            return True
    return False

def closest_seed_location(maps, seed_ranges):
    location = 0 
    while(True):
        seed = seed_for_location(location, maps)
        if is_in_range(seed, seed_ranges):
            return location
        location += 1

lines = read_input_file_lines()
seed_ranges = read_seed_ranges(lines)
maps = read_maps(lines)
print(closest_seed_location(maps, seed_ranges))