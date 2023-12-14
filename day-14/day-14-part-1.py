    
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

lines = read_input_file_lines()
dish = dish_from_lines(lines)
tilt_north(dish)
print(total_load_on_north_beams(dish))
