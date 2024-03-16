from points import generate_random_points
from scipy import interpolate
import sys
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np

def transform_points(triplet, scale=200, offset=256):
    """
    Transform points from unit circle coordinates to image grid coordinates.

    :param triplet: List of three points (x, y) representing a triplet.
    :param scale: Scaling factor for the points.
    :param offset: Offset to shift the points.
    :return: List of transformed points.
    """
    return [(x * scale + offset, y * -scale + offset) for x, y in triplet]

def closest_point_index(current_point, points):
    """
    Find the index of the closest point to the current point.

    :param current_point: Current point (x, y).
    :param points: List of points to search from.
    :return: Index of the closest point.
    """
    distances = [np.linalg.norm(np.array(current_point) - np.array(point)) for point in points]
    return np.argmin(distances)

def sort_triplets(triplets):
    """
    Sort the triplets based on the closest point to the last point of the previous triplet.

    :param triplets: List of triplets to be sorted.
    :return: Sorted list of triplets.
    """
    sorted_triplets = [triplets.pop(0)]
    while triplets:
        last_point = sorted_triplets[-1][-1]
        next_triplet_index = closest_point_index(last_point, [triplet[0] for triplet in triplets])
        sorted_triplets.append(triplets.pop(next_triplet_index))
    return sorted_triplets

def plot_triplets(triplets, image_path):
    """
    Plot the triplets and generate an image.

    :param triplets: List of triplets to be plotted.
    :param image_path: Path to save the generated image.
    """
    triplets = [transform_points(triplet) for triplet in triplets]
    sorted_triplets = sort_triplets(triplets)

    fig, ax = plt.subplots()

    all_x = []
    all_y = []

    for i, triple in enumerate(sorted_triplets):
        next_triple = sorted_triplets[(i + 1) % len(sorted_triplets)]

        # Draw a line to the next triple
        ax.plot([triple[2][0], next_triple[0][0]], [triple[2][1], next_triple[0][1]], color='black', linewidth=1)

        # Plot the point of local concavity
        ax.plot(triple[1][0], triple[1][1], 'o', color='orange')

        if random.choice([True, False]):  # Randomly choose to draw a line or curve
            # Create path from triple and add as a patch
            triple_path = path.Path(triple, closed=False)

            # Store the x, y coordinates for the line
            all_x.extend([triple[0][0], triple[1][0], triple[2][0]])
            all_y.extend([triple[0][1], triple[1][1], triple[2][1]])

            patch = patches.PathPatch(triple_path, facecolor='white', lw=1)
            ax.add_patch(patch)
        else:
            # Parametric splines treat x and y as functions of a third parameter, typically t.
            # You can think of t as the "time" parameter that travels along the curve.
            # For a 3-point curve, you might use t-values of [0, 0.5, 1] to represent the
            # start, middle, and end of your curve.
            t = np.array([0, 0.5, 1])  # Parameter
            x = np.array([point[0] for point in triple])
            y = np.array([point[1] for point in triple])

            # Fit parametric spline
            tck, u = interpolate.splprep([x, y], s=0, k=2)

            unew = np.linspace(0, 1, 100)
            out = interpolate.splev(unew, tck)

            # Store the x, y coordinates so we can fill the shape later
            all_x.extend(out[0])
            all_y.extend(out[1])

            # Plot the results
            ax.plot(out[0], out[1], color='black')

    # Fill the area enclosed by the curves
    ax.fill(all_x, all_y, color='black')

    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.axis('off')  # Hide axes

    fig.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <number_of_images> <number_of_points> <output_directory>")
        sys.exit(1)

    # Get the number of images to generate
    number_of_images = int(sys.argv[1])
    if number_of_images < 1:
        raise ValueError("Number of images must be greater than or equal to 1.")

    # Get the number of random points to generate
    number_of_points = int(sys.argv[2])
    if number_of_points < 2:
        raise ValueError("Number of random points must be greater than or equal to 2.")

    # Get the output directory
    output_directory = sys.argv[3]

    for ni in range(number_of_images):
        points = generate_random_points(number_of_points)
        
        # Generate the image path
        image_path = f"{output_directory}/image_{ni}.png"

        # Create the image
        plot_triplets(points, image_path)