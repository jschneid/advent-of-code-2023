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
    if previous_state.last_move_direction != 'south' and previous_state.y > 0 and not (previous_state.last_move_direction == 'north' and previous_state.last_move_streak == 3):
        possible_next_moves.append(State(previous_state.y - 1, previous_state.x, 'north', 1, 0))
    if previous_state.last_move_direction != 'north' and previous_state.y < len(map) - 1 and not (previous_state.last_move_direction == 'south' and previous_state.last_move_streak == 3):
        possible_next_moves.append(State(previous_state.y + 1, previous_state.x, 'south', 1, 0))
    if previous_state.last_move_direction != 'east' and previous_state.x > 0 and not (previous_state.last_move_direction == 'west' and previous_state.last_move_streak == 3):
        possible_next_moves.append(State(previous_state.y, previous_state.x - 1, 'west', 1, 0))
    if previous_state.last_move_direction != 'west' and previous_state.x < len(map[0]) - 1 and not (previous_state.last_move_direction == 'east' and previous_state.last_move_streak == 3):
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
    if move in all_states:
        return True
    
    extra_move = State(move.y, move.x, move.last_move_direction, move.last_move_streak + 1, 0)
    if extra_move in all_states:
        return True

    extra_extra_move = State(move.y, move.x, move.last_move_direction, move.last_move_streak + 2, 0)
    if extra_extra_move in all_states:
        return True

    # Now that we've done the fast O(1) checks that we're able to do, do the slow O(N) check
    for state in all_states:
        if state.y == move.y and state.x == move.x and state.last_move_direction == move.last_move_direction and state.last_move_streak <= move.last_move_streak and state.accumulated_heat_loss <= move.accumulated_heat_loss:
            return True

    return False

def minimum_heat_loss(map):
    initial_state = State(0, 0, 'south', 0, 0)
    states_to_evaluate = possible_next_moves(map, initial_state, [])
    
    all_states = set()
    for state in states_to_evaluate:
        all_states.add(state)

    while True:
        # Sort states_to_evaluate by accumulated_heat_loss, lowest first
        states_to_evaluate = sorted(states_to_evaluate)

        state = states_to_evaluate.pop(0)

        if state.y == len(map) - 1 and state.x == len(map[0]) - 1:
            return state.accumulated_heat_loss

        new_states = possible_next_moves(map, state, all_states)
        states_to_evaluate += new_states
        for new_state in new_states:
            all_states.add(new_state)

start_time = time.time()
map = read_input_file_lines()
print(minimum_heat_loss(map))
print("--- %s seconds ---" % (time.time() - start_time))