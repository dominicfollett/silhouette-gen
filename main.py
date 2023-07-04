from points import generate_random_points
import sys
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np

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

        if random.choice([True, False]):  # randomly choose to draw a line or curve
            # create path from triple and add as a patch
            triple_path = path.Path(triple, closed=False)
            patch = patches.PathPatch(triple_path, facecolor='white', lw=1)
            ax.add_patch(patch)
        else:
            # draw Bezier curve
            codes = [path.Path.MOVETO, path.Path.CURVE3, path.Path.CURVE3]
            curve_path = path.Path(triple, codes)
            patch = patches.PathPatch(curve_path, facecolor='white', lw=1)
            ax.add_patch(patch)

        # draw a line or curve to the next triple
        if random.choice([True, False]):
            ax.plot([triple[2][0], next_triple[0][0]], [triple[2][1], next_triple[0][1]], color='black', linewidth=1)
            pass
        else:
            mid_point = [(triple[2][0] + next_triple[0][0]) / 2, (triple[2][1] + next_triple[0][1]) / 2]
            codes = [path.Path.MOVETO, path.Path.CURVE3, path.Path.CURVE3]
            curve_path = path.Path([triple[2], mid_point, next_triple[0]], codes)
            patch = patches.PathPatch(curve_path, facecolor='white', lw=1)
            ax.add_patch(patch)

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

