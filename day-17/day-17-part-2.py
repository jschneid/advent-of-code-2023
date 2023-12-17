import time

class State:
    def __init__(self, y, x, last_move_direction, last_move_streak, accumulated_heat_loss):
        self.y = y
        self.x = x
        self.last_move_direction = last_move_direction
        self.last_move_streak = last_move_streak
        self.accumulated_heat_loss = accumulated_heat_loss

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.last_move_direction == other.last_move_direction and self.last_move_streak == other.last_move_streak

    def __hash__(self):
        return self.x + 200 * self.y + 30000 * hash(self.last_move_direction) + 10000000 * self.last_move_streak
    
    def __lt__(self, other):
        return self.accumulated_heat_loss < other.accumulated_heat_loss

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def possible_next_moves(map, previous_state, all_states):
    possible_next_moves = []

    if previous_state.last_move_streak >= 1 and previous_state.last_move_streak <= 3:
        # We are forced to proceed straight!
        if previous_state.last_move_direction == 'south' and previous_state.y < len(map) - 1:
            possible_next_moves.append(State(previous_state.y + 1, previous_state.x, 'south', 1, 0))
        elif previous_state.last_move_direction == 'north' and previous_state.y > 0:
            possible_next_moves.append(State(previous_state.y - 1, previous_state.x, 'north', 1, 0))
        elif previous_state.last_move_direction == 'east' and previous_state.x < len(map[0]) - 1:
            possible_next_moves.append(State(previous_state.y, previous_state.x + 1, 'east', 1, 0))
        elif previous_state.last_move_direction == 'west' and previous_state.x > 0:
            possible_next_moves.append(State(previous_state.y, previous_state.x - 1, 'west', 1, 0))
    else:
        # We can proceed straight (if we haven't gone too far in the current direction) or turn!
        if previous_state.last_move_direction != 'south' and previous_state.y > 0 and not (previous_state.last_move_direction == 'north' and previous_state.last_move_streak == 10):
            possible_next_moves.append(State(previous_state.y - 1, previous_state.x, 'north', 1, 0))
        if previous_state.last_move_direction != 'north' and previous_state.y < len(map) - 1 and not (previous_state.last_move_direction == 'south' and previous_state.last_move_streak == 10):
            possible_next_moves.append(State(previous_state.y + 1, previous_state.x, 'south', 1, 0))
        if previous_state.last_move_direction != 'east' and previous_state.x > 0 and not (previous_state.last_move_direction == 'west' and previous_state.last_move_streak == 10):
            possible_next_moves.append(State(previous_state.y, previous_state.x - 1, 'west', 1, 0))
        if previous_state.last_move_direction != 'west' and previous_state.x < len(map[0]) - 1 and not (previous_state.last_move_direction == 'east' and previous_state.last_move_streak == 10):
            possible_next_moves.append(State(previous_state.y, previous_state.x + 1, 'east', 1, 0))
    
    for possible_next_move in possible_next_moves:
        possible_next_move.accumulated_heat_loss = previous_state.accumulated_heat_loss + int(map[possible_next_move.y][possible_next_move.x])
        if previous_state.last_move_direction == possible_next_move.last_move_direction:
            possible_next_move.last_move_streak = previous_state.last_move_streak + 1 

    eligible_next_moves = []
    for move in possible_next_moves:
        if state_already_evaluated(move, all_states):
            continue
        eligible_next_moves.append(move)
    
    return eligible_next_moves

def state_already_evaluated(move, all_states):
    return move in all_states

def minimum_heat_loss(map):
    initial_state = State(0, 0, 'none', 0, 0)
    states_to_evaluate = possible_next_moves(map, initial_state, [])
    
    all_states = set()
    for state in states_to_evaluate:
        all_states.add(state)

    while True:
        # Sort states_to_evaluate by accumulated_heat_loss, lowest first
        states_to_evaluate = sorted(states_to_evaluate)

        state = states_to_evaluate.pop(0)
        
        if state.y == len(map) - 1 and state.x == len(map[0]) - 1 and state.last_move_streak >= 4:
            return state.accumulated_heat_loss

        new_states = possible_next_moves(map, state, all_states)
        states_to_evaluate += new_states
        for new_state in new_states:
            all_states.add(new_state)

start_time = time.time()
map = read_input_file_lines()
print(minimum_heat_loss(map))
print("--- %s seconds ---" % (time.time() - start_time))