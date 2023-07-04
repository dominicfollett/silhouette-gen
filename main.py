from points import generate_random_points
from scipy import interpolate
import sys
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np

np.random.seed(44)

def plot_points(triplets, image_path):
    # Transform points to image grid
    def transform_points(triplet):
        #return [(x * 256 + 256, y * -256 + 256) for x, y in triplet]
        return [(x * 200 + 256, y * -200 + 256) for x, y in triplet] # 200 is the scale factor

    triplets = [transform_points(triplet) for triplet in triplets]

    fig, ax = plt.subplots()

    for triple in triplets:
        # plot first and last point in green
        ax.plot(triple[0][0], triple[0][1], 'go')
        ax.plot(triple[2][0], triple[2][1], 'go')

        # plot middle point in orange
        ax.plot(triple[1][0], triple[1][1], 'o', color='orange')

    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.axis('off')  # Hide axes

    fig.savefig(image_path, dpi=300, bbox_inches='tight')

def closest_point_index(current_point, points):
    distances = [np.linalg.norm(np.array(current_point)-np.array(point)) for point in points]
    return np.argmin(distances)

def sort_triplets(triplets):
    sorted_triplets = [triplets.pop(0)]
    while triplets:
        last_point = sorted_triplets[-1][-1]
        next_triplet_index = closest_point_index(last_point, [triplet[0] for triplet in triplets])
        sorted_triplets.append(triplets.pop(next_triplet_index))
    return sorted_triplets

def plot_triplets(triplets, image_path):
    # Transform points to image grid
    def transform_points(triplet):
        return [(x * 200 + 256, y * -200 + 256) for x, y in triplet]

    triplets = [transform_points(triplet) for triplet in triplets]
    sorted_triplets = sort_triplets(triplets)

    fig, ax = plt.subplots()

    for i, triple in enumerate(sorted_triplets):
        next_triple = sorted_triplets[(i + 1) % len(sorted_triplets)]

        # Draw a line to the next triple
        ax.plot([triple[2][0], next_triple[0][0]], [triple[2][1], next_triple[0][1]], color='black', linewidth=1)
        # Plot the point of local concavity
        ax.plot(triple[1][0], triple[1][1], 'o', color='orange')

        if random.choice([True, False]):  # randomly choose to draw a line or curve
            # create path from triple and add as a patch
            triple_path = path.Path(triple, closed=False)
            patch = patches.PathPatch(triple_path, facecolor='white', lw=1)
            ax.add_patch(patch)
        else:
            """
               Parametric splines treat x and y as functions of a third parameter, typically t.
               You can think of t as the "time" parameter that travels along the curve.
               For a 3-point curve, you might use t-values of [0, 0.5, 1] to represent the
               start, middle, and end of your curve.
            """
            t = np.array([0, 0.5, 1])  # parameter
            x = np.array([point[0] for point in triple])
            y = np.array([point[1] for point in triple])

            # Fit parametric spline
            tck, u = interpolate.splprep([x, y], s=0, k=2)

            unew = np.linspace(0, 1, 100)
            out = interpolate.splev(unew, tck)

            # Plot the results
            ax.plot(x, y, 'x', out[0], out[1])

    ax.set_xlim(0, 512)
    ax.set_ylim(0, 512)
    ax.axis('off')  # Hide axes

    fig.savefig(image_path, dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    # Get the number of images to generate
    number_of_images = int(sys.argv[1])

    if number_of_images < 1:
        raise ValueError("Number of images must be greater than or equal to 1.")

    # Get the number of random points to generate
    number_of_points = int(sys.argv[2])

    if number_of_points < 1:
        raise ValueError("Number of random points must be greater than or equal to 1.")
    
    # Get the output directory
    output_directory = sys.argv[3]

    for ni in range(number_of_images):
        points = generate_random_points(number_of_points)
        
        # generate the image path
        image_path = output_directory + "/image_" + str(ni) + ".png"

        # create the image
        plot_triplets(points, image_path)
        # plot_points(points, image_path)

