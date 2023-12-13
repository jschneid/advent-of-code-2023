from itertools import combinations

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
        return self.end_index - self.start_index + 1
    
    def __str__(self) -> str:
        return self.type * self.width()

class Row:
    def __init__(self, segments, damaged_segment_sizes): 
        self
        self.segments = segments
        self.damaged_segment_sizes = damaged_segment_sizes

    def end_index(self):
        return self.segments[-1].end_index

    def width(self):
        return self.end_index() + 1

    def segment_at_index(self, index):
        for segment in self.segments:
            if segment.start_index <= index and index <= segment.end_index:
                return segment

    def type_at_index(self, index):
        segment = self.segment_at_index(index)
        return segment.type

    def compatible_with(self, other):
        for index in range(self.width()):
            if self.type_at_index(index) == '#' and other.type_at_index(index) == '.':
                return False
            if self.type_at_index(index) == '.' and other.type_at_index(index) == '#':
                return False
        return True
            
    def __str__(self) -> str:
        return ''.join(str(segment) for segment in self.segments)

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

        damaged_segment_sizes = read_damaged_segment_sizes(csv)

        rows.append(Row(segments, damaged_segment_sizes))
    return rows

def read_damaged_segment_sizes(csv):
    return list(int(width) for width in csv.split(','))

def possible_arrangement_counts_sum(rows):
    return sum(possible_arrangement_counts(row) for row in rows)

def possible_arrangement_counts(row):
    all_possible_arrangements = possible_row_arrangements_for_damaged_segment_sizes(row.damaged_segment_sizes, row.width())
    
    # Our approach here:
    # 1. Using only the damaged segment sizes (and ignoring the map of positions), 
    #    generate all possible arrangements of operational and broken segments.
    # 2. Compare each of those possible arrangements with the map of posistions from 
    #    the input. Throw out any mismatches, where in any position the possible 
    #    arrangement has a '#' but the input has a '.', or vice-versa.
    # 3. The count that remain are the possible arrangements count for that row.
    count = 0
    for possible_arrangement in all_possible_arrangements:
        if possible_arrangement.compatible_with(row):
            count += 1
    
    return count

def possible_row_arrangements_for_damaged_segment_sizes(damaged_segment_sizes, row_width):
    number_of_groups = len(damaged_segment_sizes)
    number_of_spaces_between_groups = number_of_groups - 1
    number_of_additional_empty_spaces = row_width - sum(damaged_segment_sizes) - number_of_spaces_between_groups

    # Hat tip to https://towardsdatascience.com/solving-nonograms-with-120-lines-of-code-a7c6e0f627e4 for this line!
    arrangements = combinations(range(number_of_groups + number_of_additional_empty_spaces), number_of_groups)
    rows = []

    for arrangement in arrangements:
        segments = []
        if arrangement[0] > 0:
            segments.append(Segment(0, arrangement[0] - 1, '.'))
        position = arrangement[0]         
        for i in range(len(arrangement)):
            broken_segment_start = position
            broken_segment_end = broken_segment_start + damaged_segment_sizes[i] - 1
            segments.append(Segment(broken_segment_start, broken_segment_end, '#'))
            
            operational_segment_start = broken_segment_end + 1
            if i < len(arrangement) - 1:
                operational_segment_width = arrangement[i + 1] - arrangement[i]
            else:
                operational_segment_width = row_width - operational_segment_start
            if operational_segment_width > 0:
                operational_segment_end = operational_segment_start + operational_segment_width - 1
                segments.append(Segment(operational_segment_start, operational_segment_end, '.'))
                position = operational_segment_end + 1
        rows.append(Row(segments, damaged_segment_sizes))
    return rows

lines = read_input_file_lines()
rows = read_rows(lines)
print (possible_arrangement_counts_sum(rows))
