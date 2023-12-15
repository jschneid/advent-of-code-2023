import csv

class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

class Box:
    def __init__(self):
        self.lenses = []

    def remove_lens_with_label(self, label):
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)
                return
    
    def set_lens_with_focal_length(self, label, focal_length):
        for lens in self.lenses:
            if lens.label == label:
                lens.focal_length = focal_length
                return
        self.lenses.append(Lens(label, focal_length))
        
def array_from_csv_file():
    with open('input.txt') as csvfile:
        return list(csv.reader(csvfile))[0]

def hash(input_string):
    current_value = 0
    for character in input_string:
        current_value = (current_value + ord(character)) * 17 % 256
    return current_value

def initialize_boxes():
    boxes = []
    for _ in range(256):
        boxes.append(Box())
    return boxes

def arrange_boxes_with_lenses(steps):
    boxes = initialize_boxes()
    for step in steps:
        if step[-1] == '-':
            label = step[0:-1]
            box_number = hash(label)
            boxes[box_number].remove_lens_with_label(label)
        else:
            label = step[0:-2]
            focal_length = int(step[-1])
            box_number = hash(label)
            boxes[box_number].set_lens_with_focal_length(label, focal_length)
    return boxes

def total_focusing_power(boxes):
    total = 0 
    for box_index in range(256):
        for lens_index in range(len(boxes[box_index].lenses)):
            total += (1 + box_index) * (1 + lens_index) * boxes[box_index].lenses[lens_index].focal_length
    return total

steps = array_from_csv_file()
boxes = arrange_boxes_with_lenses(steps)
print(total_focusing_power(boxes))