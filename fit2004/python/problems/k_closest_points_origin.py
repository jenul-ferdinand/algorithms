"""
? Name
K Closest Points to Origin

? Description
Given a list of points in the 2D plane (x, y).

Return the k points closet to the the origin (0, 0).

Distance is measured by Euclidean distance. 

You must implement an expected O(n) time algorithm using QuickSelect to
partition the points by their squared distance to the origin.
"""
from typing import List, Tuple
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def k_closest_points(
    points: List[Tuple[int, int]], 
    k: int
) -> List[Tuple[int, int]]:
    N = len(points)
    
    # Euclidean distance list for each point
    distances = [math.sqrt(x**2 + y**2) for x, y in points]
    
    # Find threshold using quick select
    threshold = quick_select(distances[:], 0, N-1, k-1)
    
    # Populate the output list based on threshold
    output = []
    for x, y in points:
        distance = math.sqrt(x**2 + y**2)
        if distance <= threshold:
            output.append((x,y))
    
    # Return the output list    
    return output

if __name__ == '__main__':
    # Test: Basic
    pts = [(1,3), (-2,2), (5,8), (0,1)]
    k = 2
    res = k_closest_points(pts, k)
    exp = {(-2,2), (0,1)}
    assert set(res) == exp, f'Expected {exp}, got {res}'
    
    # Test: Multiple points at the same distance
    # Here (1,2) and (2,1) both have distance² = 5, while (3,4) and (4,3) are 
    # farther.
    pts = [(1, 2), (2, 1), (3, 4), (4, 3)]
    k = 2
    result = k_closest_points(pts, k)
    expected = {(1, 2), (2, 1)}
    assert set(result) == expected, f"Expected {expected}, got {result}"

    
    print('All tests passed')