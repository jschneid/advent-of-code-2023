class Brick:
    def __init__(self, x0, y0, z0, x1, y1, z1):
        if (x0 < x1):
            self.x0 = x0
            self.x1 = x1
        else:
            self.x0 = x1
            self.x1 = x0
        if (y0 < y1):
            self.y0 = y0
            self.y1 = y1
        else:
            self.y0 = y1
            self.y1 = y0
        if (z0 < z1):
            self.z0 = z0
            self.z1 = z1
        else:
            self.z0 = z1
            self.z1 = z0

    def contains_cube(self, x, y, z):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1 and self.z0 <= z <= self.z1

    def bottom_cubes(self):
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                yield [x, y, self.z0]

    def top_cubes(self):
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                yield [x, y, self.z1]

    def __lt__(self, other):
        return self.z0 < other.z0

def brick_at(bricks, x, y, z):
    for brick in bricks:
        if brick.contains_cube(x, y, z):
            return brick
    return None

def drop_brick_to(brick, destination_z0, occupied_cubes):
    remove_occupied_cubes(brick, occupied_cubes)
    delta = brick.z0 - destination_z0
    brick.z1 = brick.z1 - delta
    brick.z0 = destination_z0
    add_occupied_cubes(brick, occupied_cubes)

def cubes_below_brick_unoccupied(brick, destination_z0, occupied_cubes):
    for x in range(brick.x0, brick.x1 + 1):
        for y in range(brick.y0, brick.y1 + 1):
            if is_occupied(x, y, destination_z0, occupied_cubes):
                return False
    return True

def plummet(brick, occupied_cubes):
    destination_z0 = brick.z0

    while cubes_below_brick_unoccupied(brick, destination_z0 - 1, occupied_cubes):
        destination_z0 -= 1
    
    if brick.z0 == destination_z0:
        return

    drop_brick_to(brick, destination_z0, occupied_cubes)

def plummet_all(bricks, occupied_cubes):
    for brick in bricks:
        plummet(brick, occupied_cubes)

def bricks_below(brick):
    result = set()
    for [x, y, z] in brick.bottom_cubes():
        if z == 1:
            continue
        other_brick = brick_at(bricks, x, y, z - 1)
        if other_brick is not None:
            result.add(other_brick)
    return result

def bricks_above(brick):
    result = set()
    for [x, y, z] in brick.top_cubes():
        other_brick = brick_at(bricks, x, y, z + 1)
        if other_brick is not None:
            result.add(other_brick)
    return result

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_bricks():
    lines = read_input_file_lines()
    bricks = []
    for line in lines:
        x0, y0, z0 = line.split('~')[0].split(',')
        x1, y1, z1 = line.split('~')[1].split(',')
        bricks.append(Brick(int(x0), int(y0), int(z0), int(x1), int(y1), int(z1)))
    bricks.sort()
    return bricks

def all_multiple_supported(bricks):
    for brick in bricks:
        supporting_bricks = bricks_below(brick)
        if len(supporting_bricks) == 1: 
            return False
    return True

def disintegration_candidate_count(bricks):
    count = 0
    for brick in bricks:
        supported_bricks = bricks_above(brick)
        if all_multiple_supported(supported_bricks):
            count += 1
    return count

def populate_occupied_cubes(bricks):
    # Note that this does not track the middle cubes of vertical bricks
    occupied_cubes = set()
    for brick in bricks:
        add_occupied_cubes(brick, occupied_cubes)
    return occupied_cubes

def is_occupied(x, y, z, occupied_cubes):
    if z < 1:
        return True
    return (x, y, z) in occupied_cubes
            
def remove_occupied_cubes(brick, occupied_cubes):
    for [x, y, z] in brick.top_cubes():
        occupied_cubes.remove((x, y, z))
    if brick.z0 == brick.z1:
        return
    for [x, y, z] in brick.bottom_cubes():
        occupied_cubes.remove((x, y, z))

def add_occupied_cubes(brick, occupied_cubes):
    for [x, y, z] in brick.top_cubes():
        occupied_cubes.add((x, y, z))
    if brick.z0 == brick.z1:
        return
    for [x, y, z] in brick.bottom_cubes():
        occupied_cubes.add((x, y, z))

bricks = read_bricks()
occupied_cubes = populate_occupied_cubes(bricks)
plummet_all(bricks, occupied_cubes)
print(disintegration_candidate_count(bricks))