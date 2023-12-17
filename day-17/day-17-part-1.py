class State:
    def __init__(self, y, x, last_move_direction, last_move_streak, accumulated_heat_loss):
        self.y = y
        self.x = x
        self.last_move_direction = last_move_direction
        self.last_move_streak = last_move_streak
        self.accumulated_heat_loss = accumulated_heat_loss

    def __str__(self) -> str:
        return f'(y={self.y}, x={self.x}, last_move_direction={self.last_move_direction}, last_move_streak={self.last_move_streak}, accumulated_heat_loss={self.accumulated_heat_loss})'

    def __repr__(self) -> str:
        return self.__str__()

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
    # TODO If this is slow optimize the datatype to have it be faster than O(N)
    for state in all_states:
        # TODO maybe also throw out moves with greater heat when streak is the same?
        if state.y == move.y and state.x == move.x and state.last_move_direction == move.last_move_direction and state.last_move_streak <= move.last_move_streak and state.accumulated_heat_loss <= move.accumulated_heat_loss:
            return True
    return False

def minimum_heat_loss(map):
    initial_state = State(0, 0, 'south', 0, 0)
    max_solution_heat_loss = 1400
    states_to_evaluate = possible_next_moves(map, initial_state, [])
    
    all_states = []
    for state in states_to_evaluate:
        all_states.append(state)

    while len(states_to_evaluate) > 0:
        # Sort states_to_evaluate by accumulated_heat_loss, lowest first
        states_to_evaluate.sort(key=lambda x: x.accumulated_heat_loss)

        state = states_to_evaluate.pop(0)

        if state.accumulated_heat_loss >= max_solution_heat_loss:
            continue

        if state.y == len(map) - 1 and state.x == len(map[0]) - 1:
            max_solution_heat_loss = state.accumulated_heat_loss
            print("New minimum! " + str(max_solution_heat_loss))
        else:
            new_states = possible_next_moves(map, state, all_states)
            states_to_evaluate += new_states
            all_states += new_states

    return max_solution_heat_loss    

map = read_input_file_lines()
print(minimum_heat_loss(map))