def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def predict_next_value(numbers):
    if all(number == 0 for number in numbers):
        return 0
    
    next_line = []
    for index in range(1, len(numbers)):
        next_line.append(numbers[index] - numbers[index - 1])
    
    return numbers[-1] + predict_next_value(next_line)    

def extrapolated_sequences_sum(lines):
    total = 0

    for line in lines:
        numbers = [int(number) for number in line.split()]
        total += predict_next_value(numbers)

    return total

lines = read_input_file_lines()
print(extrapolated_sequences_sum(lines))