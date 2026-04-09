"""
? Name:
Minimum Travel Time

? Description:
You are given a directed, non-negative, weighted graph of N cities (1..N) and
M roads.

Each road is described by a triple (u,v,t)

Meaning there is a one-way connection from city u to city v that takes t units
of time to traverse.

Given a start city S and a destination city T, compute the minimum travel time
from S to T. 

If T cannot be reached from S, report infinity.

This is a class single-source shortest-path problem on a graph with 
non-negative weights and is solved by Dijkstra algorithm in O((N+M) log N) time.
"""

from typing import List, Tuple
import heapq
import math

INF = math.inf

def min_travel_time(
    num_cities: int,
    roads: List[Tuple[int,int,int]],
    start: int,
    end: int
):
    n = num_cities + 1
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u,v,t in roads:
        adj[u].append((v,t))
        
    visited = [INF] * n
    visited[start] = 0
    
    heap = [(0, start)]
    while heap:
        curr_dist, curr_city = heapq.heappop(heap)
        
        if curr_dist > visited[curr_city]:
            continue
        
        if curr_city == end:
            return curr_dist
        
        for neighbour, dist in adj[curr_city]:
            new_dist = curr_dist + dist
            
            if new_dist < visited[neighbour]:
                visited[neighbour] = new_dist

                heapq.heappush(heap, (new_dist, neighbour))
                
    return INF
                
if __name__ == '__main__':
    n = 5
    roads = [
        (1, 2, 2),
        (1, 3, 5),
        (2, 3, 1),
        (2, 4, 2),
        (3, 5, 3),
        (4, 5, 1)
    ]
    start = 1
    end = 5
    
    res = min_travel_time(n,roads,start,end)
    exp = 5
    
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed')