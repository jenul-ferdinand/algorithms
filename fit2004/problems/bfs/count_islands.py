from typing import List, Tuple
from collections import deque

"""
? Name:
Count Islands in a Grid

? Description:
Given an r x c grid of '1's (land) and '0's (water), count how many islands 
there are. 

An island is a maximal group of horizontally or vertically adjacent '1' cells.

You must implement a BFS to traverse each island; you may not use Python dict
or set. Only lists (for your grid and a visited matrix and a deque queue).

? Input:
- r: The number of rows
- c: The number of columns
- grid: A list of length r, where each entry is a list of length c containing
characters '1', or '0'.
"""

def count_islands(r: int, c: int, grid: List[List[str]]) -> int:
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    visited = [[False] * c for _ in range(r)]
    islands = 0
    
    def bfs(sr: int, sc: int) -> None:
        queue = deque()
        visited[sr][sc] = True
        queue.append((sr, sc))
        
        while queue:
            cr, cc = queue.popleft()
            for dr, dc, in directions:
                nr, nc = cr + dr, cc + dc

                if 0 <= nr < r and 0 <= nc < c:
                    if grid[nr][nc] == '1' and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        
    for row in range(r):
        for col in range(c):
            if grid[row][col] == '1' and not visited[row][col]:
                islands += 1
                bfs(row, col)
                    
    return islands

if __name__ == "__main__":
    # Example 1:
    # r = 4, c = 5
    # grid:
    # 1 1 0 0 0
    # 1 1 0 0 1
    # 0 0 1 0 1
    # 0 0 0 1 1
    #
    # There are three islands:
    #  - Top-left block at {(0,0),(0,1),(1,0),(1,1)}
    #  - Single-cell island at {(2,2)}
    #  - Right-hand cluster {(1,4),(2,4),(3,4),(3,3)}
    #
    # Expected output: 3

    r1, c1 = 4, 5
    grid1 = [
        ['1','1','0','0','0'],
        ['1','1','0','0','1'],
        ['0','0','1','0','1'],
        ['0','0','0','1','1']
    ]
    assert count_islands(r1, c1, grid1) == 3, f"Expected 3, got {count_islands(r1, c1, grid1)}"

    # Example 2:
    # r = 3, c = 3
    # grid:
    # 1 0 1
    # 0 0 0
    # 1 0 1
    #
    # Four separate single-cell islands at the corners.
    # Expected output: 4

    r2, c2 = 3, 3
    grid2 = [
        ['1','0','1'],
        ['0','0','0'],
        ['1','0','1']
    ]
    assert count_islands(r2, c2, grid2) == 4, f"Expected 4, got {count_islands(r2, c2, grid2)}"

    # Example 3:
    # r = 3, c = 4
    # grid:
    # 1 1 1 0
    # 1 0 1 0
    # 1 0 0 1
    #
    # Two islands:
    #  - Large “C”-shaped region in top-left
    #  - Single cell at (2,3)
    #
    # Expected output: 2

    r3, c3 = 3, 4
    grid3 = [
        ['1','1','1','0'],
        ['1','0','1','0'],
        ['1','0','0','1']
    ]
    assert count_islands(r3, c3, grid3) == 2, f"Expected 2, got {count_islands(r3, c3, grid3)}"

    print("All tests passed!")