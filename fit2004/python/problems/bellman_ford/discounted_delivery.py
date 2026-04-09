"""

A logistics company must deliver packages from a central depot (city 1) to all
other cities. The road network has both regular tolls and special "coupon" 
roads that reduce your toll cost. Each road is one-way, with:

- A base toll `t >= 0`
- A coupon dicount `d >= 0` (so the effective cost is `t-d`, possibly negative)

There are no cycles whose total discount exceeds total tolls (i.e., no 
negative-cost cycles).

Design a O(N * M) algorithm using Bellman-Ford to compute the minimum cost to 
reach every city from the depot.

Input:
- `N`: Number of cities (nodes)
- `M`: Number of roads (edges)
- `roads`: List of tuples `(u,v,t,d)` where:
    - `u`: Starting city (node)
    - `v`: Ending city (node)
    - `t`: Base toll cost
    - `d`: Coupon discount

Output:
- A list of N numbers, where the j-th value is the minimum cost to reach city
j from city 1, or math.inf if unreachable.

Modelling:
- Build a directed graph with N vertices.
- For each road `(u,v,t,d)`, add an edge u -> v with weight `w=t-d`.
- Run Bellman-Ford from source node 1

"""

from typing import List, Tuple
import math
from collections import deque

City = int
Toll = int
Discount = int
Road = Tuple[City, City, Toll, Discount]

INF = math.inf

def discounted_delivery(
    N: int, 
    M: int, 
    roads: List[Road]
) -> List[int]:
    """
    ! Discounted Delivery
    
    Finds the minimum cost to reach every city from city 1, or INF if unreachable.
    
    Time Complexity: O(N * M)
    Time Complexity Analysis:
        - Creating distance array: O(N)
        - Creating predecessor array: O(N)
        - Main loop:
            - Looping through each city & road: O(N * M)
            - Relaxation case: O(1)
        - Final iteration to detect negative cycles: 
            - Building adjacency list: O(M)
            - Looping through each road: O(M)
            - Checking and updating bad nodes: O(N + M)
            - Setting distances for bad nodes: O(N)
            
        So O(N + N + N * M + M + M + N + M + N) = O(N * M)
        
    Auxiliary Space Complexity: O(N + M)
    Auxiliary Space Complexity Analysis:
        - Distance array: O(N)
        - Ajdacency list: O(N + M)
        - Bad nodes array: O(N)
    
    Terms:
        - V: The number of cities.
        - M: The numer of roads.
    
    """
    V = N + 1 
    
    dist = [INF for _ in range(V)]
    dist[1] = 0
    
    # (1) Relax edges V - 1 times
    for _ in range(V - 1):
        updated = False
        for u,v,t,d in roads:
            w = t - d
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
                
    # (2) Detect which vertices are on or reachable from negative cycles
    bad = [False] * V
    adj: List[List[int]] = [[] for _ in range(V)]
    for u,v,_,_ in roads:
        adj[u].append(v)
    
    for u,v,t,d in roads:
        w = t - d
        if dist[u] != INF and dist[v] > dist[u] + w:
            bad[v] = True
    
    queue = deque(i for i, flag in enumerate(bad) if flag)
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if not bad[y]:
                bad[y] = True
                queue.append(y)
                
    # (3) Set distances to INF for all bad nodes
    for i in range(V):
        if bad[i]:
            dist[i] = INF
        
    # Output distance array
    return dist[1:]
        

if __name__ == '__main__':
    # (1) Basic test
    roads = [
        (1, 2, 10, 2),  # Road from city 1 to city 2 with toll 10 and discount 2
        (1, 3, 5, 1),   # Road from city 1 to city 3 with toll 5 and discount 1
        (2, 4, 3, 0),   # Road from city 2 to city 4 with toll 3 and no discount
        (3, 4, 2, 1),   # Road from city 3 to city 4 with toll 2 and discount 1
        (4, 5, 8, 3),   # Road from city 4 to city 5 with toll 8 and discount 3
        (2, 5, 7, 2)    # Road from city 2 to city 5 with toll 7 and discount 2
    ]
    N = 5  # Number of cities
    M = 6  # Number of roads
    
    result = discounted_delivery(N, M, roads)
    assert result == [0, 8, 4, 5, 10], f"Expected [0, 8, 4, 6, 10], got {result}"
    
    # (2) Negative cycle test
    # Cities: 1 -> 2 -> 3 -> 2 forms a cycle of total weight < 0
    # Roads:
    # 1 -> 2 with cost 1-0 = 1
    # 2 -> 3 with cost 2-4 = -2
    # 3 -> 2 with cost 1-0 = 1
    # 
    # Cycle 2 -> 3 -> 2 has weight -2 + 1 = -1 < 0, so all nodes in that cycle
    # should end up as INF.
    roads = [
        (1,2,1,0),
        (2,3,2,4),
        (3,2,1,0)
    ]
    N = 3
    M = len(roads)
    
    result = discounted_delivery(N, M, roads)
    assert result == [0, INF, INF], f'Expected [0, inf, inf], got {result}'
    
    print('All tests passed!')