def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def scratchcards_quantity(cards):
    card_quantities = [1] * (len(cards))

    for (card_index, card) in enumerate(cards):
        numbers_we_have = get_numbers_we_have(card)
        winning_numbers = get_winning_numbers(card)
        overlapping_numbers = len(intersection(numbers_we_have, winning_numbers))
        for update_index in range(card_index + 1, card_index + overlapping_numbers + 1):
            card_quantities[update_index] += card_quantities[card_index]

    return sum(card_quantities)

def get_numbers_we_have(card):
    return card.split(":")[1].split("|")[0].split()

def get_winning_numbers(card):
    return card.split(":")[1].split("|")[1].split()

def intersection(list1, list2):
    return [value for value in list1 if value in list2]

cards = read_input_file_lines()
print(scratchcards_quantity(cards))
