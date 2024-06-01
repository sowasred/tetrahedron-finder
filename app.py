import itertools
from collections import defaultdict

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
    
def find_combinations_with_sum(points, target_sum):
    n_to_points = defaultdict(list)
    for i, point in enumerate(points):
        n = point[3]
        n_to_points[n].append((i, point))
    
    candidates = []
    keys = list(n_to_points.keys())
    for comb in itertools.combinations(keys, 4):
        if sum(comb) == target_sum:
            for combo in itertools.product(*[n_to_points[n] for n in comb]):
                indices, pts = zip(*combo)
                if len(set(indices)) == 4:
                    candidates.append((indices, pts))
    return candidates

def find_smallest_tetrahedrons(points):
    tetrahedrons = []
    candidates = find_combinations_with_sum(points, 100)
    
    for indices, pts in candidates:
        p1, p2, p3, p4 = pts
        vol = volume_of_tetrahedron(p1, p2, p3, p4)
        tetrahedrons.append((vol, sorted(indices)))
    
    tetrahedrons.sort()
    return [indices for _, indices in tetrahedrons[:4]]

# Parse points from files
points_small = parse_points('./points_small.txt')
points_large = parse_points('./points_large.txt')

# Find the smallest tetrahedron
smallest_tetrahedrons_small = find_smallest_tetrahedrons(points_small)
smallest_tetrahedron_large = find_smallest_tetrahedrons(points_large)

print(f'Smallest tetrahedron for points_small.txt: {smallest_tetrahedrons_small}')
print(f'Smallest tetrahedron for points_large.txt: {smallest_tetrahedron_large}')


for i, tetrahedron in enumerate(smallest_tetrahedrons_small):
    print(f'Smallest tetrahedron {i+1} for points_small.txt: {tetrahedron}')

for i, tetrahedron in enumerate(smallest_tetrahedron_large):
    print(f'Smallest tetrahedron {i+1} for points_large.txt: {tetrahedron}')