import numpy as np

class Hailstone:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz

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
    x, y, z = [int(position) for position in line.split('@')[0].split(', ')]
    dx, dy, dz = [int(velocity) for velocity in line.split('@')[1].split(', ')]
    return Hailstone(x, y, z, dx, dy, dz)

# Math adapted from https://www.reddit.com/r/adventofcode/comments/18q40he/2023_day_24_part_2_a_straightforward_nonsolver/
def solve(hailstones, dimension):
    # d0 here is the "other" dimension that was passed in (either y or z).
    # dd0 likewise is the other dimension's velocity (dy or dz).
    x0 = hailstones[0].x
    d0 = getattr(hailstones[0], dimension)
    dx0 = hailstones[0].dx
    dd0 = getattr(hailstones[0], 'd' + dimension)

    # This Wikipedia article was helpful in understanding the coefficients and the 
    # contant terms of a system of linear equations: https://en.wikipedia.org/wiki/System_of_linear_equations#General_form
    coefficients = []
    constant_terms = []
    
    # We have 4 unknowns -- the x, y, dx, and dy of our rock -- and so we need 4 equations.
    # As above, the "d" variables are either the y or z of our second hailstone.
    for hailstone in hailstones[1:5]:
        x1 = hailstone.x
        d1 = getattr(hailstone, dimension)
        dx1 = hailstone.dx
        dd1 = getattr(hailstone, 'd' + dimension)
        
        constant_terms.append(x1 * dd1 - d1 * dx1 - x0 * dd0 + d0 * dx0)
        coefficients.append([dd1 - dd0, dx0 - dx1, d0 - d1, x1 - x0])

    # Numpy linear equation system solver from https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html
    solution = np.linalg.solve(np.array(coefficients), np.array(constant_terms))
    return solution

hailstones = read_hailstones()
x, y, dx, dy = solve(hailstones, 'y')  
_x, z, _dx, dz = solve(hailstones, 'z')
print(x + y + z)