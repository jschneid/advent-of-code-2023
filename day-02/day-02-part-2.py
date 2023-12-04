class CubeBag:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def raise_game_minimums(self, red, green, blue):
        if red > self.red:
            self.red = red
        if green > self.green:
            self.green = green
        if blue > self.blue:
            self.blue = blue

    def power(self):
        return self.red * self.green * self.blue

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def game_powers_sum(lines):
    total = 0

    for line in lines:
        game_cube_bag = CubeBag()

        split_line = line.split(":")
        game_id = split_line[0].split()[1]

        reveals = split_line[1].split(";")
        calculate_minimums(reveals, game_cube_bag)
                
        total += int(game_cube_bag.power())
        
    return total

def calculate_minimums(reveals, game_cube_bag):
    for reveal in reveals:
        update_minimums(reveal, game_cube_bag)
    
def update_minimums(reveal, game_cube_bag):
    quantities = reveal.split(",")
    for quantity in quantities:
        red = 0
        green = 0
        blue = 0
        split_quantity = quantity.split()
        if (split_quantity[1] == "red"):
            red = (int(split_quantity[0]))
        if (split_quantity[1] == "green"):
            green = (int(split_quantity[0]))
        if (split_quantity[1] == "blue"):
            blue = (int(split_quantity[0]))
        game_cube_bag.raise_game_minimums(red, green, blue)

lines = read_input_file_lines()
print(game_powers_sum(lines))