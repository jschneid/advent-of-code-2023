with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

print(lines)

calibration_total = 0

for line in lines:
    for character in line:
        if character.isdigit():
            first_digit_character = character
            break
    for character in reversed(line):
        if character.isdigit():
            last_digit_character = character
            break
    calibration_value_string = first_digit_character + last_digit_character
    calibration_total += int(calibration_value_string)

print(calibration_total)