import numpy as np
import matplotlib.pyplot as plt

# Set the seed
# np.random.seed(44)

def calculate_angle(a, b, c):
    """Calculate the angle at point b, between the lines ab, and bc."""
    # Convert points to numpy arrays
    a, b, c = np.array(a), np.array(b), np.array(c)

    # Calculate vectors ab and bc
    ab = a - b
    bc = c - b

    # Calculate the dot product of ab and bc
    dot_product = np.dot(ab, bc)

    # Calculate the cross product of ab and bc
    cross_product = np.cross(ab, bc)

    # Calculate the lengths of ab and bc
    length_ab = np.linalg.norm(ab)
    length_bc = np.linalg.norm(bc)

    # Calculate the angle in radians using the dot product formula
    angle_rad = np.arccos(dot_product / (length_ab * length_bc))

    # If the cross product is negative, add the angle to pi (180 degrees) to get the counterclockwise angle
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

def too_small(w1, w2, epsilon) -> bool:
    """Check if the width of the arc is too small."""
    return w1 - w2 < epsilon 

def get_largest_arc(already_selected_arcs, buffer) -> tuple:
    """Get the list of available arcs."""
    if len(already_selected_arcs) == 0:
        return (np.pi/2, (np.pi / 2) + np.pi)
    
    largest_arc = None
    largest_arc_width = 0
    start_angle = 0

    # TODO: handle the potential wrap around case


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

alphabet_hash = {}
for number in range(1, 27):
    letter = chr(ord('a') + number - 1)
    alphabet_hash[number] = letter

# -- For testing purposes --------------------------------------
# Create a figure and axis
fig, ax = plt.subplots()

# Plot the unit circle
theta = np.linspace(0, 2 * np.pi, 100)
x = np.cos(theta)
y = np.sin(theta)
ax.plot(x, y, color='black')
# ---------------------------------------------------------------

# Set the number of random points to generate
number_of_random_points = 15

neighborhood_width = 2*np.pi/(number_of_random_points)

# I have no idea if this heuristic is going to work well
buffer =  (2*np.pi) / (number_of_random_points ** 3)

r = 1  # The radius of the unit circle

epsilon = 1e-3  # A small value

# To keep track of which arcs have already been selected
already_selected_arcs = []

# To keep track of the triplets of points we want to use for the deformation
triplets = []
final_triplets = []

# print("Neighborhood width: ", neighborhood_width)
# print("Buffer: ", buffer)

for n in range(number_of_random_points):
    selected_arc = get_largest_arc(already_selected_arcs, buffer)

    if selected_arc is None:
        print(f"No available arcs left... total number of points generated: {n} out of {number_of_random_points}")
        break

    arc_width = selected_arc[1] - selected_arc[0]
    # print("Arc width: ", arc_width)
    # print("Arc is not too small: ", not too_small(selected_arc[1], selected_arc[0], epsilon))

    # Get a random angle from the selected arc closer to the midpoint of the arc
    theta = np.random.uniform(selected_arc[0] + arc_width/2, selected_arc[1] - arc_width/2)

    # Get two angles that are within a neighborhood of theta
    theta_neighborhood_one, theta_neighborhood_two = get_neighboring_points(theta, neighborhood_width, buffer, selected_arc)

    already_selected_arcs.append((theta_neighborhood_one, theta_neighborhood_two))
    already_selected_arcs.sort()

    # Get the points on the unit circle from the angles
    px, py = get_point(theta, r)
    p1_x, p1_y = get_point(theta_neighborhood_one, r)
    p2_x, p2_y = get_point(theta_neighborhood_two, r)

    triplets.append([(p1_x, p1_y), (px, py), (p2_x, p2_y)])

    # Calculate the new 'between point' by scaling the radius by a random value
    r_prime = r * np.random.uniform(0.1, 0.91)
    b_x, b_y = get_point(theta, r_prime)

    angle = calculate_angle((p1_x, p1_y), (b_x, b_y), (p2_x, p2_y ))

    cx, cy = b_x, b_y

    # We want to ensure that the between point is a local point of maximum concavity
    # If the angle between the three points on a counter clockwise arc is greater than pi,
    # then the between point is not a local point of maximum concavity
    if angle >= np.pi:
        # This is a simple hack to get the between point to be a local point of maximum concavity
        b_x = 0
        b_y = 0

    # Plot the points
    ax.plot(p1_x, p1_y, marker='o', markersize=4, color='limegreen')
    ax.plot(px, py, marker='o', markersize=4, color='red')
    ax.plot(b_x, b_y, marker='o', markersize=4, color='blue')
    if b_x != cx and b_y != cy:
        ax.plot(cx, cy, marker='o', markersize=4, color='orange')
    ax.plot(p2_x, p2_y, marker='o', markersize=4, color='limegreen')

    # Set the aspect ratio as equal and adjust the plot limits
    ax.set_aspect('equal')
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])

    # Remove the axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig(f"unit_circle_{n}.png", dpi=300, bbox_inches='tight')
"""
# Plot the points
for triplet in triplets:
    ax.plot(triplet[0][0], triplet[0][1], marker='o', markersize=6, color='limegreen')
    ax.plot(triplet[1][0], triplet[1][1], marker='*', markersize=6, color='red')
    ax.plot(triplet[2][0], triplet[2][1], marker='o', markersize=6, color='limegreen')

# Set the aspect ratio as equal and adjust the plot limits
ax.set_aspect('equal')
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])

# Remove the axis ticks
ax.set_xticks([])
ax.set_yticks([])

# Save the plot as an image
plt.savefig('unit_circle.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
"""



