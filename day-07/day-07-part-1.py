from collections import Counter
class Hand:
    def __init__(self, cards_string, bid):
        self.cards = self.cards_string_to_cards(cards_string)
        self.bid = int(bid)
        self.sorted_cards = sorted(self.cards, reverse=True)

    def cards_string_to_cards(self, cards_string):
        cards = []
        for card_character in cards_string:
            cards.append(self.card_character_to_int(card_character))
        return cards

    def card_character_to_int(self, card_character):
        match card_character:
            case 'A':
                return 14
            case 'K':
                return 13
            case 'Q':
                return 12
            case 'J':
                return 11
            case 'T':
                return 10
            case _:
                return int(card_character)
            
    def strength(self):
        counter = sorted(list(Counter(self.cards).values()), reverse=True)
        if counter == [5]:
            return 6
        if counter == [4, 1]:
            return 5
        if counter == [3, 2]:
            return 4
        if counter == [3, 1, 1]:
            return 3
        if counter == [2, 2, 1]:
            return 2
        if counter == [2, 1, 1, 1]:
            return 1
        return 0
    
    def __lt__(self, other):
        if self.strength() != other.strength():
            return self.strength() < other.strength()
        for index in range(0, 5):
            if self.cards[index] != other.cards[index]:
                return self.cards[index] < other.cards[index]
        return False
    
def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def hands_from_lines(lines):
    hands = []
    for line in lines:
        split_line = line.split()
        hands.append(Hand(split_line[0], split_line[1]))
    return hands

def winnings(hands):
    sorted_hands = sorted(hands)
    winnings = 0
    for rank, hand in enumerate(sorted_hands, start = 1):
        winnings += hand.bid * rank
    return winnings

lines = read_input_file_lines()
hands = hands_from_lines(lines)
print(winnings(hands))