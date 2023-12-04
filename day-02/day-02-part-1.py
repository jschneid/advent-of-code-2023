def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def possible_games_ids_sum(lines):
    total = 0

    for line in lines:
        split_line = line.split(":")
        game_id = split_line[0].split()[1]

        reveals = split_line[1].split(";")
        if (not is_game_valid(reveals)):
            continue
                
        total += int(game_id)
        
    return total

def is_game_valid(reveals):
    for reveal in reveals:
        if (not is_reveal_valid(reveal)):
            return False
    return True
    
def is_reveal_valid(reveal):
    quantities = reveal.split(",")
    for quantity in quantities:
        split_quantity = quantity.split()
        if (split_quantity[1] == "red"):
            if (int(split_quantity[0])) > 12:
                return False
        if (split_quantity[1] == "green"):
            if (int(split_quantity[0])) > 13:
                return False
        if (split_quantity[1] == "blue"):
            if (int(split_quantity[0])) > 14:
                return False
    return True

lines = read_input_file_lines()
print(possible_games_ids_sum(lines))