import numpy as np
import matplotlib.pyplot as plt

# Set the seed
# np.random.seed(42)

def get_point(theta) -> tuple:
    """Calculate a a point on the unit circle curve."""
    x, y = np.sin(theta), np.cos(theta)
    return x, y

def get_neighboring_points(theta, width, buffer, selected_arc) -> tuple:
    """Calculate two angles in a unit circle curve that are within a neighborhood of theta."""

    sa_first = selected_arc[0]
    sa_last = selected_arc[1]

    theta_one_bound_point = theta - width + buffer
    if theta_one_bound_point < sa_first:
        theta_one_bound_point = sa_first + buffer

    theta_one = np.random.uniform(theta - buffer, theta_one_bound_point)

    theta_two_bound_point = theta + width - buffer
    if theta_two_bound_point > sa_last:
        theta_two_bound_point = sa_last - buffer
    
    theta_two = np.random.uniform(theta + buffer, theta_two_bound_point)
    
    return theta_one, theta_two

def randomly_select_arc(available_arcs) -> tuple:
    """Randomly select an arc from a list of available arcs."""
    selected_arc_index = np.random.randint(0, len(available_arcs))
    selected_arc = available_arcs.pop(selected_arc_index)
    return selected_arc

def too_small(w1, w2, epsilon) -> bool:
    """Check if the width of the arc is too small."""
    return w1 - w2 < epsilon 

def get_largest_arc(already_selected_arcs, buffer) -> tuple:
    """Get the list of available arcs."""
    if len(already_selected_arcs) == 0:
        return (0, 2 * np.pi)
    
    largest_arc = None
    largest_arc_width = 0
    start_angle = 0
    for arc in already_selected_arcs:
        terminating_angle = arc[0]

        # TODO: If the arcs is big enough, add it to the list of available arcs
        neighborhood_width - (terminating_angle - start_angle)
        
        if not too_small(neighborhood_width, terminating_angle - start_angle, epsilon):
            arc = (start_angle, terminating_angle - buffer)
            width = arc[1] - arc[0]
            if width >= largest_arc_width:
                largest_arc = arc
                largest_arc_width = width

        start_angle = arc[1] + buffer

    # TODO: If the last arc is big enough, add it to the list of available arcs
    if not too_small(neighborhood_width, 2*np.pi - start_angle, epsilon):
        arc = (start_angle, 2*np.pi)
        width = arc[1] - arc[0]
        if width >= largest_arc_width:
            largest_arc = arc
            largest_arc_width = width
    
    return largest_arc

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
number_of_random_points = 8

neighborhood_width = 2*np.pi/number_of_random_points

# I have no idea if this heuristic is going to work well
buffer =  (2*np.pi) / (number_of_random_points ** 3)

r = 1  # The radius of the unit circle

epsilon = 1e-3  # A small value

# To keep track of which arcs have already been selected
already_selected_arcs = []

# To keep track of the triplets of points we want to use for the deformation
triplets = []

for n in range(number_of_random_points):
    selected_arc = get_largest_arc(already_selected_arcs, buffer)

    if selected_arc is None:
        print(f"No available arcs left... total number of points generated: {n} out of {number_of_random_points}")
        break

    # TODO: Perhaps use a modulo to ensure that the angle is always between 0 and 2π
    # Get a random angle from the selected arc
    theta = np.random.uniform(*selected_arc)

    # Get two angles that are within a neighborhood of theta
    theta_neighborhood_one, theta_neighborhood_two = get_neighboring_points(theta, neighborhood_width, buffer, selected_arc)

    already_selected_arcs.append((theta_neighborhood_one + buffer, theta_neighborhood_two - buffer))

    # Get the points on the unit circle from the angles
    px, py = get_point(theta)
    p1_x, p1_y = get_point(theta_neighborhood_one)
    p2_x, p2_y = get_point(theta_neighborhood_two)

    triplets.append([(p1_x, p1_y), (px, py), (p2_x, p2_y)])

    # Plot the points
    ax.plot(p1_x, p1_y, marker='o', markersize=3, color='limegreen')
    ax.plot(px, py, marker='o', markersize=3, color='red')
    ax.plot(p2_x, p2_y, marker='o', markersize=3, color='limegreen')

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



