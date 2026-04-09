"""
? Name
Earliest Arrival Scheduling

? Description
You are given a schedule of M flights between N airports (1..N).

Each flight is a 4-tuple (u,v,d,a) meaning there is a flight from airport u to v
that departs at time d and arrives at time a (0 <= d < a).

You start at airport S at time 0. You may take any flight whose departure time
is >= your current arrival time at that airport. 

Compute the earliest possible arrival time at airport T. if T is unreachable, 
return infinity.

This can be modeled as a shortset path problem in a time-expanded graph and
solved in O(N+M log N) time using a dijkstra style algorithm on states
(current_time, airport).
"""

from typing import List, Tuple
import math
import heapq

INF = math.inf

def earliest_arrival(
    N: int,
    M: int,
    flights: List[Tuple[int,int,int,int]],
    start: int,
    end: int
) -> float:
    """
    Earliest Arrival Time
    
    Approach Description:
    - Sort the flights by the departure time earliest to latest, so we can skip
    flights early.
    - Create adjacency list for all flights.
    - Initialise a best array for best arrival times for each airport.
    - Initialise starting state as 0 time
    - Use min heap popping current time and current airport.
    - We check the neighbouring airports and compare the departure time with 
    the current time to see if we can actually catch the flight.
    - We check if the arrival time is faster than the current best time for the
    neighbouring airport. If so, we push that new state to the heap also marking
    the new best.
    - We return best[end]
    
    Return:
        The earliest arrival time at `end` starting from `start` at time 0 or 
        INF if unreachable.
    """
    N = N + 1
    
    # Sort the flights by departure time
    flights = sorted(flights, key = lambda x : x[2])
    
    adj = [[] for _ in range(N)]
    for u,v,d,a in flights:
        adj[u].append((d,a,v))
        
    best = [INF] * N
    best[start] = 0
    
    heap = [(0, start)]
    while heap:
        curr_time, curr = heapq.heappop(heap)
        
        if curr_time > best[curr]:
            continue
        
        if curr == end:
            return best[curr]
        
        for departure, arrival, airport in adj[curr]:
            if departure >= curr_time:
                if arrival < best[airport]: 
                    best[airport] = arrival
                    heapq.heappush(heap, (arrival, airport))
    
    return best[end]
        
if __name__ == '__main__':
    # Test case:
    # 4 airports, 5 flights:
    # 1→2 departs 1 arrives 5
    # 1→3 departs 2 arrives 3
    # 3→2 departs 4 arrives 6
    # 2→4 departs 6 arrives 8
    # 3→4 departs 7 arrives 9
    #
    # Best route to airport 4 is 1→2 (1–5), wait 5→6, then 2→4 (6–8) ⇒ arrival at 8.
    N = 4
    flights = [
        (1, 2, 1, 5),
        (1, 3, 2, 3),
        (3, 2, 4, 6),
        (2, 4, 6, 8),
        (3, 4, 7, 9),
    ]
    M = len(flights)
    start, end = 1, 4

    res = earliest_arrival(N, M, flights, start, end)
    exp = 8
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')