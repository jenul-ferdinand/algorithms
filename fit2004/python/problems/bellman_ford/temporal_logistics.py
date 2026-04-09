"""
Temporal Logistics

A courier company operates a network of N cities connected by M directed roads. 

Each road has a "travel time" t (representing a time-saving device), 
zero, or positive.

The courier starts at city 1 at time 0 and wants to know:

1. The minimum possible arrival time to each city j.
2. Whether certain cities can be reached at arbitrarily early
(i.e., "negative infinite") times due to time-travel loops (negative cycles).

Any city that lies on or is reachable from a negative-cycle reachable from city
1 should be reported as "PARADOX".

Design an O(N*M)-time algorithm using Bellman-Ford (with one extra pass to 
detect negative cycles).
"""

from typing import List, Tuple
from collections import deque
import math
import sys
import io

INF = math.inf

def temporal_logistics(
    N: int,
    M: int,
    roads: List[Tuple[int, int, int]]
) -> None:
    """
    Temporal Logistics
    
    Finds:
    - Prints minimum possible arrival to each city j.
    - Prints UNREACHABLE for each city j that is part of a negative cycle.
    - Prints PARADOX for any city that lies on or is reachable from a negative
        cycle reachable from city 1.
    
    Time Complexity: O(N * M)
    Space Complexity: O(N + M)
    """
    V = N + 1
    
    dist = [INF] * V
    dist[1] = 0
    
    for _ in range(V - 1):
        for u,v,t in roads:
            if dist[v] > dist[u] + t:
                dist[v] = dist[u] + t
                
    in_neg_cycle = [False] * V
    adj = [[] for _ in range(V)]
    for u,v,t in roads:
        adj[u].append(v)
        
        if dist[v] > dist[u] + t:
            in_neg_cycle[v] = True
            
    queue = deque(i for i, flag in enumerate(in_neg_cycle) if flag)
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if not in_neg_cycle[y]:
                in_neg_cycle[y] = True
                queue.append(y)
            
    for j in range(V):
        if dist[j] == INF:
            print('UNREACHABLE')
        elif in_neg_cycle[j]:
            print('PARADOX')
        else:
            print(dist[j])
            

if __name__ == '__main__':
    # Test case with a negative cycle among cities 2→3→4→2,
    # a branch out to city 5, a normal path to 6→7, and an unreachable city 8.
    N = 8
    roads = [
        # no cycle edges
        (1, 2,  3),   # 1→2 (time 3)
        (2, 5, 10),   # 2→5 (time 10)
        (1, 6, 20),   # 1→6 (time 20)
        (6, 7,  5),   # 6→7 (time 5)
        # negative‐cycle edges
        (2, 3,  4),   # 2→3 (time 4)
        (3, 4, -6),   # 3→4 (time -6)
        (4, 2,  1),   # 4→2 (time 1)
    ]
    

    # Expected printed output (one line per city j=0..8):
    # j=0: UNREACHABLE        (node 0 is unused)
    # j=1: 0                  (start city)
    # j=2: PARADOX            (in neg‐cycle)
    # j=3: PARADOX            (in neg‐cycle)
    # j=4: PARADOX            (in neg‐cycle)
    # j=5: PARADOX            (reachable from the cycle via 2→5)
    # j=6: 20                 (normal path 1→6)
    # j=7: 25                 (path 1→6→7)
    # j=8: UNREACHABLE        (no incoming roads)
    
    captured_output = io.StringIO()
    sys.stdout = captured_output
    temporal_logistics(N, len(roads), roads)
    sys.stdout = sys.__stdout__
    
    actual_output = captured_output.getvalue()
    
    expected_lines = """UNREACHABLE
    0
    PARADOX
    PARADOX
    PARADOX
    PARADOX
    20
    25
    UNREACHABLE""".splitlines()
    
    actual_lines = actual_output.splitlines()
    
    assert len(expected_lines) == len(actual_lines)
    
    for expected, actual in zip(expected_lines, actual_lines):
        assert expected.strip() == actual.strip(), f'Line mismatch: Expected {expected} got {actual}'
        
    print('All tests passed')
    