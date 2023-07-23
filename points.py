import numpy as np

def calculate_angle(a, b, c):
    """Calculate the angle at point b, between the lines ab, and bc."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    ab = a - b
    bc = c - b
    dot_product = np.dot(ab, bc)
    cross_product = np.cross(ab, bc)
    length_ab = np.linalg.norm(ab)
    length_bc = np.linalg.norm(bc)
    angle_rad = np.arccos(dot_product / (length_ab * length_bc))

    if cross_product > 0:
        angle_rad = 2 * np.pi - angle_rad

    return angle_rad

def get_point(theta, r) -> tuple:
    """Calculate a a point on the unit circle curve."""
    x, y = r * np.sin(theta), r * np.cos(theta)
    return x, y

def get_neighboring_points(theta, width, buffer, selected_arc) -> tuple:
    """Calculate two angles in a unit circle curve that are within a neighborhood of theta."""
    sa_first = selected_arc[0]
    sa_last = selected_arc[1]

    theta_one_bound_point = theta - width + buffer
    theta_one = np.random.uniform(theta - buffer, theta_one_bound_point)
    if theta_one_bound_point < sa_first:
        theta_one = np.random.uniform(sa_first, theta)

    theta_two_bound_point = theta + width - buffer
    theta_two = np.random.uniform(theta + buffer, theta_two_bound_point)
    if theta_two_bound_point > sa_last:
        theta_two = np.random.uniform(theta + buffer, sa_last)

    return theta_one, theta_two

def get_largest_arc(already_selected_arcs, buffer) -> tuple:
    """Get the largest available angle interval in the unit circle"""
    if len(already_selected_arcs) == 0:
        return (np.pi/2, (np.pi / 2) + np.pi)
    
    largest_arc = None
    largest_arc_width = 0
    start_angle = 0

    for arc in already_selected_arcs:
        terminating_angle = arc[0]
        potential_arc = (start_angle + buffer, terminating_angle - buffer)
        width = potential_arc[1] - potential_arc[0]
        if width >= largest_arc_width:
            largest_arc = potential_arc
            largest_arc_width = width
        start_angle = arc[1]

    potential_arc = (start_angle + buffer, 2*np.pi - buffer) 
    width = potential_arc[1] - potential_arc[0]
    if width >= largest_arc_width:
        largest_arc = potential_arc
        largest_arc_width = width
    
    return largest_arc

def generate_random_points(max_random_points: int) -> list:
    if max_random_points < 2:
        raise ValueError("Number of random points must be greater than or equal to 2.")

    number_of_random_points = np.random.randint(2, max_random_points)

    neighborhood_width = 2*np.pi/(number_of_random_points)
    buffer =  (2*np.pi) / (number_of_random_points*2)
    r = 1  
    already_selected_arcs = []
    triplets = []

    for n in range(number_of_random_points):
        selected_arc = get_largest_arc(already_selected_arcs, buffer)
        if selected_arc is None:
            print(f"No available arcs left... total number of points generated: {n} out of {number_of_random_points}")
            break

        arc_width = selected_arc[1] - selected_arc[0]
        theta = np.random.uniform(selected_arc[0] + arc_width/2, selected_arc[1] - arc_width/2)
        theta_neighborhood_one, theta_neighborhood_two = get_neighboring_points(theta, neighborhood_width, buffer, selected_arc)

        already_selected_arcs.append((theta_neighborhood_one, theta_neighborhood_two))
        already_selected_arcs.sort()

        p1_x, p1_y = get_point(theta_neighborhood_one, r)
        p2_x, p2_y = get_point(theta_neighborhood_two, r)

        r_prime = r * np.random.uniform(0.1, 0.91)
        b_x, b_y = get_point(theta, r_prime)
        angle = calculate_angle((p1_x, p1_y), (b_x, b_y), (p2_x, p2_y ))

        if angle >= np.pi:
            b_x = 0
            b_y = 0

        triplets.append([(p1_x, p1_y), (b_x, b_y), (p2_x, p2_y)])


    return triplets
