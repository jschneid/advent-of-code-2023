def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def scratchcards_points(lines):
    total_points = 0

    for line in lines:
        numbers_we_have = get_numbers_we_have(line)
        winning_numbers = get_winning_numbers(line)
        total_points += card_points(numbers_we_have, winning_numbers)

    return total_points

def get_numbers_we_have(line):
    return line.split(":")[1].split("|")[0].split()

def get_winning_numbers(line):
    return line.split(":")[1].split("|")[1].split()

def card_points(numbers_we_have, winning_numbers):
    overlapping_numbers = intersection(numbers_we_have, winning_numbers)
    
    if len(overlapping_numbers) == 0:
        return 0
    
    return 2 ** (len(overlapping_numbers) - 1)

def intersection(list1, list2):
    return [value for value in list1 if value in list2]

lines = read_input_file_lines()
print(scratchcards_points(lines))
