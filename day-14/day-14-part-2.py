import re

class Dish:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [['.' for x in range(width)] for y in range(height)]
    
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.cells)

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def dish_from_lines(lines):
    dish = Dish(len(lines[0]), len(lines))
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            dish.cells[y][x] = lines[y][x]
    return dish

def tilt_north(dish):
    for y in range(dish.height):
        for x in range(dish.width):
            if dish.cells[y][x] == 'O':
                move_rounded_rock_north(dish, y, x)

def move_rounded_rock_north(dish, y, x):
    new_y = y
    while new_y > 0 and dish.cells[new_y - 1][x] == '.':
        new_y -= 1
    if new_y != y:
        dish.cells[y][x] = '.'
        dish.cells[new_y][x] = 'O'   

def total_load_on_north_beams(dish):
    total_load = 0
    for y in range(dish.height):
        for x in range(dish.width):
            if dish.cells[y][x] == 'O':
                total_load += dish.height - y 
    return total_load

def rotate_2d_array_clockwise(array):
    return [list(reversed(column)) for column in zip(*array)]

def perform_cycle(dish):
    for _ in range(4):
        tilt_north(dish)
        dish.cells = rotate_2d_array_clockwise(dish.cells)

def solve(dish):
    MINIMUM_CYCLE_LENGTH = 5
    CYCLE_COUNT = 1000000000

    # Perform the cycle a bunch of times -- but not all 1 billion! -- and keep track of 
    # the load value after each cycle. When we see a load value come up that we had already
    # previously seen, check the several preceding load values before each copy to see if 
    # those are _also_ the same. If they are, we've most likely found a cycle, and we can
    # do a bit of modulo math to extrapolate the pattern out to what it will be at the 
    # billionth iteration.
    loads = []
    while True:
        perform_cycle(dish)
        load = total_load_on_north_beams(dish) 
        
        # If we've seen this same load value before already, after an earlier cycle:
        if load in loads:
            this_index = len(loads)
            previous_index = loads.index(load)
            potential_cycle_length = this_index - previous_index

            # Enforce a MINIMUM_CYCLE_LENGTH so that we don't end up picking two of the same
            # value that happen to come twice in a row. 
            #
            # The second part of this check grabs a slice of the loads list that is the several
            # values preceeding the first copy of the repeated value, and another slice that 
            # similarly slices the several values preceeding the second copy; if those slices
            # are equal (indicating that we saw the same several values in a row, in the same
            # order, twice), then we've most likely found our cycle. 
            if potential_cycle_length >= MINIMUM_CYCLE_LENGTH and loads[(MINIMUM_CYCLE_LENGTH * -1):-1] == loads[(-1 * potential_cycle_length - MINIMUM_CYCLE_LENGTH):(-1 * potential_cycle_length - 1)]:
                cycle_offset_from_beginning = previous_index
                cycle_length = potential_cycle_length
                return loads[cycle_offset_from_beginning + ((CYCLE_COUNT - cycle_offset_from_beginning) % cycle_length) - 1]

        loads.append(load)

lines = read_input_file_lines()
dish = dish_from_lines(lines)
print(solve(dish))
