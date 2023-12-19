def read_input_file_lines():
    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]
    return lines

class Point:
    def __init__(self, y, x):
        self.y = y  
        self.x = x

# We'll use this to store all of the vertical segments in the trench polygon.
# We'll use these later to determine if points are inside the polygon, using 
# ray tracing: Drawing a horizontal line starting from the far left to our 
# target point, if we intersect an odd count of these vertical segments, then 
# the point is inside the polygon.
class VerticalSegment:
    def __init__(self, x, y0, y1):
        self.x = x
        self.y0 = y0
        self.y1 = y1

    def __lt__(self, other):
        if self.x == other.x and self.y0 == other.y0:
            return self.y1 < other.y1
        elif self.x == other.x:
            return self.y0 < other.y0
        return self.x < other.x

# The trench shape is a "rectilinear polygon".
def trench_verticies_from_lines(lines):
    x = 0 
    y = 0
    perimeter = 0
    vertices = []
    vertical_segments = [] 

    for line in lines:
        split_line = line.split('#')

        length = int(split_line[1][0:5], 16)
        perimeter += length
        
        direction = int(split_line[1][5])
        if direction == 0:
            x += length
        elif direction == 1:
            vertical_segments.append(VerticalSegment(x, y, length + y))
            y += length
        elif direction == 2:
            x -= length
        elif direction == 3:
            vertical_segments.append(VerticalSegment(x, y - length, y))
            y -= length
        
        vertices.append(Point(y, x))
    
    vertical_segments.sort()
    return vertices, perimeter, vertical_segments

def is_point_inside_trench_via_raytracing(x, y, vertical_segments):
    intersections = 0
    for vertical_segment in vertical_segments:
        if vertical_segment.x > x:
            break
        if vertical_segment.y0 <= y and vertical_segment.y1 > y:
            intersections += 1
    return intersections % 2 == 1

def trench_area(verticies, vertical_segments, perimeter):
    # Split each of the verticies into x and y points, and sort them.
    x_points = []
    y_points = []
    for vertex in vertices:
        x_points.append(vertex.x)
        y_points.append(vertex.y)   
    x_points.sort()
    y_points.sort()

    # Now that we have sorted lists of x and y points of every vertex, each set of 4 consecutive points (x0, y0, x1, y1) 
    # represents a rectangle. Effectively, we've sliced our entire plane area into a ton of small rectangles, each of 
    # which is either entirely inside or entirely outside of the trench. So, for each rectangle, check if it's inside 
    # the trench by checking if a point in the rectangle is inside the trench. 
    total_area = 0
    for x_index in range(1, len(x_points) - 1):
        for y_index in range(1, len(y_points) - 1):
            if is_point_inside_trench_via_raytracing(x_points[x_index - 1], y_points[y_index - 1], vertical_segments):
                total_area += abs(x_points[x_index] - x_points[x_index - 1]) * (y_points[y_index] - y_points[y_index - 1])
            
    # The vertexes aren't just tiny points -- they, and the lines between them, are 1' squares. Therefore, the area that we
    # have calculated so far effectively counted everything except the 1-ft-wide right and bottom sides of the trench polygon.
    # That amount is equal to 1/2 of the permimeter + 1.
    return total_area + perimeter * 0.5 + 1

lines = read_input_file_lines()
vertices, perimeter, vertical_segments = trench_verticies_from_lines(lines)
print(trench_area(vertices, vertical_segments, perimeter))