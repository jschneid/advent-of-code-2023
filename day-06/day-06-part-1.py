class Race:
    def __init__(self, time, distance):
        self.time = int(time)
        self.distance = int(distance)

    def travel_distance(self, time_button_held):
        travel_time = self.time - time_button_held
        return travel_time * time_button_held
        
    def travel_distances(self):
        distances = []
        for time_button_held in range(1, self.time - 1):
            distances.append(self.travel_distance(time_button_held))
        return distances

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def record_beating_times_count(race):
    return len([travel_distance for travel_distance in race.travel_distances() if travel_distance > race.distance])

def record_beating_times_product(races):
    product = 1

    for race in races:
        product *= record_beating_times_count(race)
    
    return product

def get_races(lines):
    split_times = lines[0].split()
    split_distances = lines[1].split()

    races = []
    for race_index in range(1, len(split_times)):
        races.append(Race(split_times[race_index], split_distances[race_index]))

    return races

lines = read_input_file_lines()
races = get_races(lines)
answer = record_beating_times_product(races)
print(answer)

