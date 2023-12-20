import datetime

class Pulse:
    def __init__(self, source_module_id, destination_module_id, value):
        self.source_module_id = source_module_id
        self.destination_module_id = destination_module_id
        self.value = value

class PulseQueue:
    def __init__(self):
        self.pulses = []
        self.low_pulses_sent = 0
        self.high_pulses_sent = 0 

    def enqueue_pulse(self, pulse):
        self.pulses.append(pulse)

    def get_pulse(self):
        if len(self.pulses) == 0:
            return None
        
        pulse = self.pulses.pop(0)

        if pulse.value == 0:
            self.low_pulses_sent += 1
        else:
            self.high_pulses_sent += 1 

        return pulse
    
    def product_of_low_and_high_pulses_sent(self):
        return self.low_pulses_sent * self.high_pulses_sent

class FlipFlopModule:
    def __init__(self, id, destination_module_ids, pulse_queue):
        self.id = id
        self.destination_module_ids = destination_module_ids
        self.state = 0 # off 
        self.pulse_queue = pulse_queue

    def pulse(self, value, _input_module_id):
        if value == 1:
            return
        
        self.state ^= 1

        for destination_module_id in self.destination_module_ids:
            self.pulse_queue.enqueue_pulse(Pulse(self.id, destination_module_id, self.state))

class ConjunctionModule:
    def __init__(self, id, destination_module_ids, pulse_queue):
        self.id = id
        self.destination_module_ids = destination_module_ids
        self.input_module_states = {}
        self.pulse_queue = pulse_queue

    def add_input_module(self, input_module_id):
        self.input_module_states[input_module_id] = 0

    def pulse(self, value, input_module_id):
        self.input_module_states[input_module_id] = value

        if 0 in self.input_module_states.values():
            outgoing_pulse_value = 1
        else:
            outgoing_pulse_value = 0

        for destination_module_id in self.destination_module_ids:
            self.pulse_queue.enqueue_pulse(Pulse(self.id, destination_module_id, outgoing_pulse_value))

class BroadcastModule:
    def __init__(self, destination_module_ids, pulse_queue):
        self.id = 'broadcaster'
        self.destination_module_ids = destination_module_ids
        self.pulse_queue = pulse_queue

    def pulse(self, _value, _input_module_id):
        for destination_module_id in self.destination_module_ids:
            self.pulse_queue.enqueue_pulse(Pulse(self.id, destination_module_id, 0))

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def modules_from_lines(lines, pulse_queue):
    modules = {}
    for line in lines:
        add_module_from_line(modules, line, pulse_queue)
    for module_id, module in modules.items():
        if isinstance(module, ConjunctionModule):
            for other_module in modules.values():
                if module_id in other_module.destination_module_ids:
                    module.add_input_module(other_module.id)
    return modules

def add_module_from_line(modules, line, pulse_queue):
    if line.startswith('%'):
        add_flip_flop_module_from_line(modules, line, pulse_queue)
    elif line.startswith('&'):
        add_conjunction_module_from_line(modules, line, pulse_queue)
    elif line.startswith('broadcaster'):
        add_broadcast_module_from_line(modules, line, pulse_queue)

def add_flip_flop_module_from_line(modules, line, pulse_queue):
    id = line.split()[0][1:]
    destination_module_ids = line.split(' -> ')[1].split(', ')
    modules[id] = FlipFlopModule(id, destination_module_ids, pulse_queue)

def add_conjunction_module_from_line(modules, line, pulse_queue):
    id = line.split()[0][1:]
    destination_module_ids = line.split(' -> ')[1].split(', ')
    modules[id] = ConjunctionModule(id, destination_module_ids, pulse_queue)

def add_broadcast_module_from_line(modules, line, pulse_queue):
    destination_module_ids = line.split(' -> ')[1].split(', ')
    modules['broadcaster'] = BroadcastModule(destination_module_ids, pulse_queue)

def button_presses_to_send_low_pulse_to_rx(modules, pulse_queue):
    button_presses = 0
    while True:
        button_presses += 1 
        initial_pulse = Pulse('button', 'broadcaster', 0)
        pulse_queue.enqueue_pulse(initial_pulse)
        rx_low_pulsed = process_pulses_until_quiescence(modules, pulse_queue)

        if rx_low_pulsed == True:
            return button_presses
        
        if button_presses % 100000 == 0:
            print(f'{datetime.datetime.now().time()} {button_presses:,} button presses and counting...')

def process_pulses_until_quiescence(modules, pulse_queue):
    while True:
        pulse = pulse_queue.get_pulse()
        if pulse == None:
            return False
        if pulse.destination_module_id == 'rx' and pulse.value == 0:
            return True
        process_pulse(modules, pulse)

def process_pulse(modules, pulse):
    if not pulse.destination_module_id in modules:
        return

    destination_module = modules[pulse.destination_module_id]
    destination_module.pulse(pulse.value, pulse.source_module_id)

lines = read_input_file_lines()
pulse_queue = PulseQueue()
modules = modules_from_lines(lines, pulse_queue)
print(button_presses_to_send_low_pulse_to_rx(modules, pulse_queue))
