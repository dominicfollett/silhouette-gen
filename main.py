from points import generate_random_points
from tqdm import tqdm

import sys

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

    for ni in tqdm(range(number_of_images)):
        points = generate_random_points(number_of_points)
        
        print(points)
        print("-------------------------------------------\n")