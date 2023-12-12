def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

class Segment:
    def __init__(self, start_index, end_index, type):
        self.start_index = start_index
        self.end_index = end_index
        self.type = type

    def width(self):
        return self.end - self.start + 1

class Row:
    def __init__(self, segments, damaged_group_sizes): 
        self
        self.segments = segments
        self.damaged_group_sizes = damaged_group_sizes

    def segment_at_index(self, index):
        for segment in self.segments:
            if segment.start_index <= index and index <= segment.end_index:
                return segment

def read_rows(lines):
    rows = []

    for line in lines:
        segments = []

        diagram, csv = line.split()

        segment_start = 0
        for index in range(1, len(diagram)):
            if line[index] != diagram[index - 1]:
                segments.append(Segment(segment_start, index - 1, diagram[index - 1]))
                segment_start = index
        segments.append(Segment(segment_start, len(diagram) - 1, diagram[-1]))

        damaged_group_sizes = read_damaged_group_sizes(csv)

        rows.append(Row(segments, damaged_group_sizes))
    return rows

def read_damaged_group_sizes(csv):
    return list(int(width) for width in csv.split(','))

def possible_arrangement_counts_sum(rows):
    return sum(possible_arrangement_counts(row) for row in rows)

def possible_arrangement_counts(row):
    damaged_segment_to_fit = row.damaged_segments[0]
    index = 0
    # TODO resume here 


lines = read_input_file_lines()
rows = read_rows(lines)

