from typing import List, Tuple
import heapq

# Type aliases
Location = int # Location index
Cost = int # Cost of traveling between two locations
Time = int # Time in minutes

# A road is represented as a tuple of 
# & (starting location, end location, cost of travel, time to travel)
Road = Tuple[Location, Location, Cost, Time] 

# A station is represented as a tuple of 
# & (location of station, time it takes to travel to next location)
Station = Tuple[Location, Time] 

# List of locations to form a route (list of locations)
Route = List[Location]

def intercept(
    roads: List[Road],       # Each road is a directed road
    stations: List[Station], # Can loop back to first station after last station
    start: Location, 
    friend_start: Location
    ) -> Tuple[Cost, Time, Route] | None:
    """
    * Function to find the optimal route for a user to intercept their friend.
    
    ? Args:
    ?    - roads: List of roads, each represented as a tuple (start, end, cost, time)
    ?    - stations: List of stations, each represented as a tuple (location, time)
    ?    - start: Starting location of the user
    ?    - friend_start: Starting location of the friend
        
    & Returns:
    &    - A tuple containing the total cost, total time, and the optimal route taken.
    &    - If no route is found, return None.
    
    Time Complexity: 
        - Must run in O(|R| log |L|) time.
        - |R| is the number of roads and |L| is the number of locations.
        
    Space Complexity:
        - Must use O(|L| + |R|) auxiliary space.
        - |L| is the number of locations and |R| is the number of roads.
    """
    # Determine maximum number of locations |L|
    max_location = 0
    for road in roads:
        max_location = max(max_location, road[0], road[1])
    for station in stations:
        max_location = max(max_location, station[0])

    # Initialize adjacency list as a list of empty lists.
    # Each entry will contain (destination, cost, time) tuples.
    graph = [[] for _ in range(max_location + 1)]
    for road_start, road_end, road_cost, road_time in roads:
        graph[road_start].append((road_end, road_cost, road_time))

    # Create a list to map station locations to their indices.
    station_indices = [-1] * (max_location + 1)
    for i, (station_loc, _) in enumerate(stations):
        station_indices[station_loc] = i

    # Find the index of the friend's starting station.
    friend_start_idx = station_indices[friend_start]
    if friend_start_idx == -1:
        return None  # friend_start is not in the stations list.
    
    # Optionally, you can precompute the train schedule once and use it in the search.
    # Rotate stations so that friend_start is first.
    m = len(stations)
    print(stations)
    rotated = stations[friend_start_idx:] + stations[:friend_start_idx]
    print(rotated)

    # Compute scheduled time for each station and total loop time.
    # This will store the exact times in the cycle when the friend arrives at each station.
    train_sched = [-1] * (max_location + 1)
    current_time = 0
    for station, wait_time in rotated:
        train_sched[station] = current_time
        current_time += wait_time
    cycle_time = current_time  # Total cycle duration.

    # We'll use precomputed schedule in the search
    # State is defined by (location, elapsed_time mod cycle_time)
    INF = float('inf')
    best_cost = [[INF] * cycle_time for _ in range(max_location + 1)]
    best_time = [[INF] * cycle_time for _ in range(max_location + 1)]
    start_rem = 0  # At time 0.
    best_cost[start][start_rem] = 0
    best_time[start][start_rem] = 0
    
    # Priority queue holds tuples: (total_cost, total_time, location, remainder, path)
    pq = [(0, 0, start, start_rem, [start])]
    heapq.heapify(pq)
    
    # While there are states to explore in the priority queue
    while pq:
        total_cost, total_time, current, rem, path = heapq.heappop(pq)
        
        # Skip if a better path to this state was found
        if total_cost != best_cost[current][rem] or total_time != best_time[current][rem]:
            continue
        
        # Check interception: use the precomputed train schedule.
        if train_sched[current] != -1:
            # Get the time when the train is at this station in the cycle
            train_time = train_sched[current] % cycle_time
            
            # If we arrive at the same time as the train (modulo cycle time)
            if rem == train_time:
                return (total_cost, total_time, path)
        
        # Explore neighbors.
        for neighbor, road_cost, road_time in graph[current]:
            new_cost = total_cost + road_cost
            new_time = total_time + road_time
            new_rem = new_time % cycle_time
            
            # Only consider if this is a better path to this state
            if (new_cost < best_cost[neighbor][new_rem] or 
            (new_cost == best_cost[neighbor][new_rem] and new_time < best_time[neighbor][new_rem])):
                best_cost[neighbor][new_rem] = new_cost
                best_time[neighbor][new_rem] = new_time
                heapq.heappush(pq, (new_cost, new_time, neighbor, new_rem, path + [neighbor]))

    # If we've exhausted all possibilities without finding an interception
    return None

if __name__ == '__main__':
    # Test case 1, Simple
    roads: List[Road] = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2), (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2), (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations: List[Station] = [(0, 1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start: Location = 6
    friend_start: Location = 0
    result = intercept(roads, stations, start, friend_start)
    assert result == (7, 9, [6, 7, 8, 3]), f'Expected (7, 9, [6, 7, 8, 3]), got {result}'
    print("Test case 1 (simple) passed.")
    
    # Test case 2, Unsolvable
    roads: List[Road] = [(0, 1, 35, 3), (1, 2, 5, 2), (2,0,35,4), (0,4,10,1), (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations: List[Station] = [(4, 3), (5, 2), (3, 4)]
    start: Location = 0
    friend_start: Location = 4
    result = intercept(roads, stations, start, friend_start)
    assert result == None, f'Expected None, got {result}'
    print("Test case 2 (unsolvable) passed.")
    
    # Test case 3, Repeated locations
    roads: List[Road] = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations: List[Station] = [(4, 2), (5, 1), (3, 4)]
    start: Location = 0
    friend_start: Location = 3
    result = intercept(roads, stations, start, friend_start)
    assert result == (160, 39, [0,1,2,0,1,2,0,4]), f'Expected (160, 39, [0,1,2,0,1,2,0,4]), got {result}'
    print("Test case 3 (repeated locations) passed.")
    
    # Test case 4, Same Cost, Different Time
    roads: List[Road] = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations: List[Station] = [(2,4), (1,3)]
    start: Location = 0
    friendStart: Location = 1
    result = intercept(roads, stations, start, friendStart)
    assert result == (10, 3, [0,2]), f'Expected (10, 3, [0,2]), got {result}'
    print("Test case 4 (same cost, different time) passed.")
    
    # Test circular route required
    roads = [(0,1,5,1), (1,2,5,1), (2,3,5,1), (3,0,5,7)]
    stations = [(1,3), (3,7)]
    start = 0
    friend_start = 1

    result = intercept(roads, stations, start, friend_start)
    assert result == (15, 3, [0,1,2,3]), f'Expected (15, 3, [0,1,2,3]), got {result}'
    print("Test (circular route) passed.")
    
    # Test no valid path
    roads = [(0,1,5,2), (1,2,5,3), (2,0,5,4)]
    stations = [(3,2), (4,3)]
    start = 0
    friend_start = 3
    
    result = intercept(roads, stations, start, friend_start)
    assert result == None, f'Expected None, got {result}'
    print("Test (no valid path) passed.")

        