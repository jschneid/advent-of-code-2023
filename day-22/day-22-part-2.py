class Brick:
    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

        # z0 = z-level of the brick's bottom cube; z1 = top cube
        if (z0 < z1):
            self.z0 = z0
            self.z1 = z1
        else:
            self.z0 = z1
            self.z1 = z0
        
        self.all_bricks_above = []
        self.all_bricks_below = []

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

def bricks_below(brick, occupied_cubes):
    result = set()
    for [x, y, z] in brick.bottom_cubes():
        if z == 1:
            continue
        other_brick = brick_at(x, y, z - 1, occupied_cubes)
        if other_brick is not None:
            result.add(other_brick)
    return result

def bricks_above(brick, occupied_cubes):
    result = set()
    for [x, y, z] in brick.top_cubes():
        other_brick = brick_at(x, y, z + 1, occupied_cubes)
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

def populate_occupied_cubes(bricks):
    # Note that this does not track the middle cubes of vertical bricks.
    # (No need; this problem features no lateral movement / horizontal collisions.)
    occupied_cubes = {}
    for brick in bricks:
        add_occupied_cubes(brick, occupied_cubes)
    return occupied_cubes

def is_occupied(x, y, z, occupied_cubes):
    if z < 1:
        return True
    return (x, y, z) in occupied_cubes

def brick_at(x, y, z, occupied_cubes):
    if (x, y, z) in occupied_cubes:
        return occupied_cubes[(x, y, z)]
    return None
            
def remove_occupied_cubes(brick, occupied_cubes):
    for [x, y, z] in brick.top_cubes():
        del occupied_cubes[(x, y, z)]
    if brick.z0 == brick.z1:
        return
    for [x, y, z] in brick.bottom_cubes():
        del occupied_cubes[(x, y, z)]

def add_occupied_cubes(brick, occupied_cubes):
    for [x, y, z] in brick.top_cubes():
        occupied_cubes[(x, y, z)] = brick
    if brick.z0 == brick.z1:
        return
    for [x, y, z] in brick.bottom_cubes():
        occupied_cubes[(x, y, z)] = brick

def assign_all_bricks_below(bricks, occupied_cubes):
    # It's important that we go through the bricks here from low to high.
    # The __lt__ method of the Brick class sorts by z0, so we're good here.
    for brick in bricks:
        all_below = set()
        base_bricks = bricks_below(brick, occupied_cubes)
        for base_brick in base_bricks:
            all_below.add(base_brick)
            for b in base_brick.all_bricks_below:
                all_below.add(b)
        brick.all_bricks_below = all_below

def assign_all_bricks_above(bricks, occupied_cubes):
    # It's important that we go through the bricks here from high to low (by z0).
    for brick in reversed(bricks):
        all_above = set()
        supported_bricks = bricks_above(brick, occupied_cubes)
        for supported_brick in supported_bricks:
            all_above.add(supported_brick)
            for b in supported_brick.all_bricks_above:
                all_above.add(b)
        brick.all_bricks_above = all_above 

def total_other_bricks_that_would_fall(bricks):
    total = 0
    for brick in bricks:
        for supported_brick in brick.all_bricks_above:
            # Here's the key to the solution! For each brick, for each brick being
            # supported by it (directly or indirectly), if we take that supported brick's 
            # set of all bricks below it, and subtract from it the set of all bricks above
            # and all bricks below the supporting brick, if the only item left in that set
            # is the supporting brick, then we know that removing the supporting brick will
            # collapse the supported brick.
            base_bricks = (supported_brick.all_bricks_below - brick.all_bricks_above - brick.all_bricks_below)
            if len(base_bricks) == 1:
                total += 1
    return total

bricks = read_bricks()
occupied_cubes = populate_occupied_cubes(bricks)
plummet_all(bricks, occupied_cubes)
assign_all_bricks_above(bricks, occupied_cubes)
assign_all_bricks_below(bricks, occupied_cubes)

print(total_other_bricks_that_would_fall(bricks))        

# Here's an example to help visualize what's going on with the "all_bricks_above"
# and "all_bricks_below" properties. (Note that 3D-ness doesn't matter for this, 
# hence the example is in easier-to-visualize 2D; it just matters what bricks are
# above and below one another.)

#            ======G====== 
#           ===F===     H 
#          ====E====    H
#           B    ==D==  H
#    ==Z==  B   ==C==   H
# ==Y== =====A=====     H

# A:
# - Bricks above: Z, B, C, D, E, F, G
# - Bricks below: none
# Z: 
# - Bricks above: none
# - Bricks below: Y, A
# B:
# - Bricks above: E, F, G
# - Bricks below: A
# C: 
# - Bricks above: D, E, F, G
# - Bricks below: A
# D:
# - Bricks above: E, F, G
# - Bricks below: C, A
# E:
# - Bricks above: F, G
# - Bricks below: B, D, C, A
# F: 
# - Bricks above: G
# - Bricks below: B, E, D, C, A
# G:
# - Bricks above: none
# - Bricks below: F, E, B, D, C, A, H
# H:
# - Bricks above: G
# - Bricks below: none
