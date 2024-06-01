# Tetrahedron Finder

## Overview

Tetrahedron Finder is a Python program designed to process a list of 3D points and identify the four points that form valid tetrahedrons with the smallest possible volumes. A valid tetrahedron is defined as one where the sum of their associated integer values is exactly 100.

## Features

- **Efficient Parsing**: Reads points from input files.
- **Volume Calculation**: Calculates the volume of tetrahedrons.
- **Chunk Processing**: Processes combinations of points in manageable chunks to handle large datasets efficiently.
- **Result Verification**: Ensures the sum of associated integer values is exactly 100.

## Requirements

- Python 3.x
- `itertools` (part of the standard library)
- `collections` (part of the standard library)

## Usage

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/sowasred/tetrahedron-finder.git
    cd tetrahedron-finder
    ```

2. **Prepare Input Files**:
    Ensure you have your input files (`points_small.txt` and `points_large.txt`) in the same directory as the script.

3. **Run the Script**:
    ```sh
    python find_tetrahedrons.py
    ```

4. **Output**:
    The script will output the smallest tetrahedrons for both the small and large input files, along with the associated integer values and their sums.

## File Structure

- `find_tetrahedrons.py`: Main script to find the smallest tetrahedrons.
- `points_small.txt`: Example input file with a small dataset.
- `points_large.txt`: Example input file with a large dataset.

## Implementation Details

### volume_of_tetrahedron(p1, p2, p3, p4)
Calculates the volume of a tetrahedron formed by four points.

### parse_points(file_path)
Parses the points from a given file.

### find_combinations_with_sum(points, target_sum)
Finds combinations of points where the sum of their associated integer values is exactly 100.

### process_combinations_chunk(candidates)
Processes a chunk of combinations and calculates the volumes of the tetrahedrons.

### find_smallest_tetrahedrons(points, chunk_size=1000)
Processes all combinations in chunks and identifies the smallest tetrahedrons.

## Example Output

```sh
Processing points_small.txt...
Smallest tetrahedron 1 for points_small.txt: [0, 5, 11, 76], n values: [22, 25, 30, 23], sum: 100
Smallest tetrahedron 2 for points_small.txt: [1, 7, 12, 80], n values: [20, 30, 25, 25], sum: 100
Smallest tetrahedron 3 for points_small.txt: [2, 9, 15, 85], n values: [18, 32, 25, 25], sum: 100
Smallest tetrahedron 4 for points_small.txt: [3, 11, 19, 88], n values: [20, 30, 25, 25], sum: 100

Processing points_large.txt...
Smallest tetrahedron 1 for points_large.txt: [10, 15, 20, 25], n values: [25, 25, 25, 25], sum: 100
Smallest tetrahedron 2 for points_large.txt: [11, 16, 21, 26], n values: [20, 30, 25, 25], sum: 100
Smallest tetrahedron 3 for points_large.txt: [12, 17, 22, 27], n values: [22, 28, 25, 25], sum: 100
Smallest tetrahedron 4 for points_large.txt: [13, 18, 23, 28], n values: [24, 26, 25, 25], sum: 100
