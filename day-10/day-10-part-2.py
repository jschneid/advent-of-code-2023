class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'(x={self.x}, y={self.y})'
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

def start_position(lines):
    for line_index, line in enumerate(lines):
        start_x = line.find('S')
        if start_x >= 0:
            return Point(start_x, line_index)

def tile_at(lines, point):
    if point.x < 0 or point.x > len(lines[0]) - 1 or point.y < 0 or point.y > len(lines) - 1:
        return '.'
    return lines[point.y][point.x]

def point_east_of(point):
    return Point(point.x + 1, point.y)

def point_south_of(point):
    return Point(point.x, point.y + 1)

def point_west_of(point):
    return Point(point.x - 1, point.y)

def point_north_of(point):
    return Point(point.x, point.y - 1)

def next_point_from_start_point(lines, start_point):
    # Assuming that the start point isn't on an edge
    point_to_the_east = point_east_of(start_point)

    if tile_at(lines, point_to_the_east) in { '-', 'J', '7' }:
        return point_to_the_east
    point_to_the_south = point_south_of(start_point)
    if tile_at(lines, point_to_the_south) in { '|', 'L', 'J' }:
        return point_to_the_south
    return point_west_of(start_point)
    
def next_point_from_point(lines, point, previous_point):
    if previous_point.x < point.x:
        if tile_at(lines, point) == 'J': return point_north_of(point)
        if tile_at(lines, point) == '-': return point_east_of(point)
        return point_south_of(point)
    if previous_point.y < point.y:
        if tile_at(lines, point) == 'J': return point_west_of(point)
        if tile_at(lines, point) == '|': return point_south_of(point)
        return point_east_of(point)
    if previous_point.x > point.x:
        if tile_at(lines, point) == 'L': return point_north_of(point)
        if tile_at(lines, point) == '-': return point_west_of(point)
        return point_south_of(point)
    # previous_point.y > point.y
    if tile_at(lines, point) == 'F': return point_east_of(point)
    if tile_at(lines, point) == '|': return point_north_of(point)
    return point_west_of(point)

def points_and_vertices_in_path(lines):
    start_point = start_position(lines)
    points = [start_point]
    vertices = []

    # For simplicty I'm assuming that the start point is NOT a vertex -- which is the case for my input

    current_point = next_point_from_start_point(lines, start_point)
    previous_point = start_point
    while current_point != start_point:
        points.append(current_point)

        if tile_at(lines, current_point) in { 'J', 'L', '7', 'F' }:
            vertices.append(current_point)

        next_point = next_point_from_point(lines, current_point, previous_point)
        previous_point = current_point
        current_point = next_point
    return points, vertices

# Adapted from https://stackoverflow.com/a/50352869/12484 
# Uses "Polygon ray casting".
# Good explanation of algorithm from https://stackoverflow.com/a/218081/12484 : 
# Draw a virtual ray from anywhere outside the polygon to a target point, and count how often it hits a side
# of the polygon. If the number of hits is even, it's outside of the polygon, if it's odd, it's inside. 
def polygon_ray_casting(points_in_path, verticies, max_x, max_y):
    # Arrays containing the x- and y-coordinates of the polygon's vertices.
    vertx = [point.x for point in verticies]
    verty = [point.y for point in verticies]

    # Number of vertices in the polygon
    nvert = len(verticies)

    points_inside = 0

    # For every candidate position within the bounding box
    for testy in range(0, max_y):
       for testx in range(0, max_x):
            if testx == 0:
                print(f"checking y={testy}")
            if any(point.x == testx and point.y == testy for point in points_in_path):
                continue

            c = 0
            for i in range(0, nvert):
                j = i - 1 if i != 0 else nvert - 1
                if( ((verty[i] > testy ) != (verty[j] > testy)) and (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i]) ):
                    c += 1
            # If odd, that means that we are inside the polygon
            if c % 2 == 1: 
                points_inside += 1
                print(f'(x={testx}, y={testy})')
                print(points_inside)

    return points_inside
    
lines = read_input_file_lines()
points, vertices = points_and_vertices_in_path(lines)
print(polygon_ray_casting(points, vertices, len(lines[0]), len(lines)))