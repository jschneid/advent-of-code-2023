import csv

def array_from_csv_file():
    with open('input.txt') as csvfile:
        return list(csv.reader(csvfile))[0]

def hash(input_string):
    current_value = 0
    for character in input_string:
        current_value = (current_value + ord(character)) * 17 % 256
    return current_value

def total_hashed_initialization_sequence(steps):
    return sum(hash(step) for step in steps)

steps = array_from_csv_file()
print(total_hashed_initialization_sequence(steps))