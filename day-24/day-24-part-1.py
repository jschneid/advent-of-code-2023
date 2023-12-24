import itertools as it

class Hailstone:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def read_hailstones():
    lines = read_input_file_lines()
    hailstones = []
    for line in lines:
        hailstones.append(parse_hailstone(line))
    return hailstones

def parse_hailstone(line):
    x, y, _z = [int(position) for position in line.split('@')[0].split(', ')]
    dx, dy, _dz = [int(velocity) for velocity in line.split('@')[1].split(', ')]
    return Hailstone(x, y, dx, dy)

def intersections_within_test_area(hailstones, test_area_min, test_area_max):
    intersections = 0 
    for hailstone1, hailstone2 in it.combinations(hailstones, 2):
        if hailstone1 == hailstone2:
            continue
        intersection_x, intersection_y = rays_intersection(hailstone1, hailstone2)
        if intersection_x is not None and intersection_x >= test_area_min and intersection_x <= test_area_max and intersection_y >= test_area_min and intersection_y <= test_area_max:
            intersections += 1
    return intersections

# Adapted from https://stackoverflow.com/a/2932601/12484
def rays_intersection(ray1, ray2):
    if (ray2.dx * ray1.dy - ray2.dy * ray1.dx) == 0:
        return None, None 

    u = ((ray2.y - ray1.y) * ray2.dx - (ray2.x - ray1.x) * ray2.dy) / (ray2.dx * ray1.dy - ray2.dy * ray1.dx)
    v = ((ray2.y - ray1.y) * ray1.dx - (ray2.x - ray1.x) * ray1.dy) / (ray2.dx * ray1.dy - ray2.dy * ray1.dx)
    if u >= 0 and v >= 0:
        return ray1.x + u * ray1.dx, ray1.y + u * ray1.dy
    else:
        return None, None

test_area_min = 200000000000000
test_area_max = 400000000000000
print(intersections_within_test_area(read_hailstones(), test_area_min, test_area_max))  
