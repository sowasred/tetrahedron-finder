import itertools
from itertools import accumulate
from collections import defaultdict
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import psutil

def volume_of_tetrahedron(p1, p2, p3, p4):
    AB = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    AC = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    AD = (p4[0] - p1[0], p4[1] - p1[1], p4[2] - p1[2])
    
    cross_product_x = AB[1] * AC[2] - AB[2] * AC[1]
    cross_product_y = AB[2] * AC[0] - AB[0] * AC[2]
    cross_product_z = AB[0] * AC[1] - AB[1] * AC[0]
    
    scalar_triple_product = (
        AD[0] * cross_product_x +
        AD[1] * cross_product_y +
        AD[2] * cross_product_z
    )
    
    volume = abs(scalar_triple_product) / 6.0
    return volume

def parse_points(file_path):
    with open(file_path, 'r') as file:
        points = []
        for line in file:
            parts = line.strip()[1:-1].split(',')
            x, y, z, n = float(parts[0]), float(parts[1]), float(parts[2]), int(parts[3])
            points.append((x, y, z, n))
        return points

def find_combinations_with_sum(points, target_sum=100):
    print(f"Finding combinations with sum {target_sum}...")
    points = sorted(enumerate(points), key=lambda p: p[1][3])  # Sort points by their `n` value
    valid_combinations = []

    for comb in itertools.combinations(points, 4):
        n_values = [p[1][3] for p in comb]
        if sum(n_values) == target_sum:
            indices = tuple(p[0] for p in comb)
            valid_combinations.append(indices)
        elif sum(n_values) > target_sum:
            break  # Early termination since points are sorted
    
    return valid_combinations

def process_combinations_chunk(chunk, points):
    tetrahedrons = []
    for indices in chunk:
        p1, p2, p3, p4 = (points[i] for i in indices)
        vol = volume_of_tetrahedron(p1, p2, p3, p4)
        tetrahedrons.append((vol, sorted(indices)))
    return tetrahedrons

def process_chunk_wrapper(args):
    candidates, chunk_idx, chunk_size, points = args
    chunk = candidates[chunk_idx * chunk_size : (chunk_idx + 1) * chunk_size]
    return process_combinations_chunk(chunk, points)

def print_system_usage(stage=""):
    print(f"[{stage}] CPU usage: {psutil.cpu_percent()}%")
    print(f"[{stage}] Memory usage: {psutil.virtual_memory().percent}%")
    print(f"[{stage}] Available memory: {psutil.virtual_memory().available / (1024 * 1024)} MB")
    print("="*50)

def find_smallest_tetrahedrons(points, chunk_size=1000):
    print_system_usage("Before finding combinations")
    candidates = find_combinations_with_sum(points, 100)
    print(f"Number of candidates: {len(candidates)}")
    
    tetrahedrons = []
    total_chunks = (len(candidates) + chunk_size - 1) // chunk_size  # Calculate total number of chunks
    print(f"Total chunks to process: {total_chunks}")
    print_system_usage("After finding combinations")

    if total_chunks == 0:
        print("No chunks to process, exiting.")
        return []

    args = [(candidates, i, chunk_size, points) for i in range(total_chunks)]

    with Pool(cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(process_chunk_wrapper, args), total=total_chunks, desc="Processing chunks"):
            tetrahedrons.extend(result)
            print_system_usage("During processing")
    
    tetrahedrons.sort()
    print_system_usage("After processing")
    return [indices for _, indices in tetrahedrons[:4]]

# Parse points from files
points_small = parse_points('points_small.txt')
points_large = parse_points('points_large.txt')

# Find the smallest tetrahedrons
print("Processing points_small.txt...")
smallest_tetrahedrons_small = find_smallest_tetrahedrons(points_small)

print("\nProcessing points_large.txt...")
smallest_tetrahedrons_large = find_smallest_tetrahedrons(points_large)

# Verify the sum of n values and print the results
for i, tetrahedron in enumerate(smallest_tetrahedrons_small):
    n_values = [points_small[index][3] for index in tetrahedron]
    n_sum = sum(n_values)
    print(f'Smallest tetrahedron {i+1} for points_small.txt: {tetrahedron}, n values: {n_values}, sum: {n_sum}')

for i, tetrahedron in enumerate(smallest_tetrahedrons_large):
    n_values = [points_large[index][3] for index in tetrahedron]
    n_sum = sum(n_values)
    print(f'Smallest tetrahedron {i+1} for points_large.txt: {tetrahedron}, n values: {n_values}, sum: {n_sum}')
