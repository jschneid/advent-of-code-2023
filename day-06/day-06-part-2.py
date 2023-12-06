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

def get_race(lines):
    split_times = lines[0].split()
    split_distances = lines[1].split()

    time_string = ""
    distance_string = ""
    for index in range(1, len(split_times)):
        time_string += split_times[index]
        distance_string += split_distances[index]

    return Race(time_string, distance_string)

lines = read_input_file_lines()
race = get_race(lines)
answer = record_beating_times_count(race)
print(answer)
