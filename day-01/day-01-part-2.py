def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def number_word_to_digit(string):
    if string.startswith('one'):
        return '1'
    if string.startswith('two'):
        return '2'
    if string.startswith('three'):
        return '3'
    if string.startswith('four'):
        return '4'
    if string.startswith('five'):
        return '5'
    if string.startswith('six'):
        return '6'
    if string.startswith('seven'):
        return '7'
    if string.startswith('eight'):
        return '8'
    if string.startswith('nine'):
        return '9'
    return None

def calibration_total(lines):
    total = 0

    for line in lines:
        for index, character in enumerate(line):
            if character.isdigit():
                first_digit_character = character
                break
            digit_from_word = number_word_to_digit(line[index:])
            if digit_from_word is not None:
                first_digit_character = digit_from_word
                break
        for index, character in enumerate(line):
            if character.isdigit():
                last_digit_character = character
            digit_from_word = number_word_to_digit(line[index:])
            if digit_from_word is not None:
                last_digit_character = digit_from_word

        calibration_value_string = first_digit_character + last_digit_character
        total += int(calibration_value_string)

    return total

lines = read_input_file_lines()
print(calibration_total(lines))