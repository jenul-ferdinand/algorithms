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
# & (location of station, time to wait at the station)
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
    # * Determine maximum number of locations |L|
    max_location = 0
    for road in roads:
        max_location = max(max_location, road[0], road[1])
    
    # * Initialize adjacency list as a list of empty lists
    # Each entry will contain (destination, cost, time) tuples
    graph = [[] for _ in range(max_location + 1)]
    
    # Build the adjacency list
    for road_start, road_end, road_cost, road_time in roads:
        graph[road_start].append((road_end, road_cost, road_time))
    
    # Create a list to map station locations to their indices
    station_indices = [-1] * (max_location + 1)
    for i, (station_loc, _) in enumerate(stations):
        station_indices[station_loc] = i
    
    # Find the index of the friend's starting station
    friend_start_idx = station_indices[friend_start]
    if friend_start_idx == -1:
        return None # friend_start is not in the stations list
    
    # Function to calculate friend's position at a given time
    def get_friend_position(elapsed_time: Time) -> Location:
        """Calculate the station where the friend is at a given elapsed time.
        
        Returns the station location if the friend is at a station, or -1 if in transit.
        """
        if elapsed_time == 0:
            return friend_start  # At starting position at time 0
        
        # Calculate total loop time
        total_loop_time = sum(station[1] for station in stations)
        
        # Calculate time within the current loop
        time_in_loop = elapsed_time % total_loop_time
        
        # Check if friend is at a station at this time
        current_time = 0
        current_idx = friend_start_idx
        
        # Check if at starting position
        if time_in_loop == current_time:
            return stations[current_idx][0]
        
        # Check subsequent stations
        for _ in range(len(stations)):
            station_time = stations[current_idx][1]
            current_time += station_time
            current_idx = (current_idx + 1) % len(stations)
            if time_in_loop == current_time:
                return stations[current_idx][0]
        
        # Friend is in transit
        return -1
    
    # Initialize priority queue with (cost, time, location, path)
    # We prioritize by cost first, then by time
    pq = [(0, 0, start, [start])]
    heapq.heapify(pq)
    
    # To track minimum costs and times for each location
    # visited[current_location] = [(time, cost)]
    # For each location and time, track the minimum cost
    visited = [[] for _ in range(max_location + 1)]
    iteration_count = 0
    
    # While there are states to explore in the priority queue
    # And the iteration count is less than the maximum location index
    while pq and iteration_count < max_location + 1:
        iteration_count += 1
        
        # Pop the state with the lowest cost and time
        total_cost, total_time, current, path = heapq.heappop(pq)
        
        # Check if we've intercepted the friend at a train station
        friend_pos: Location = get_friend_position(total_time)
        if current == friend_pos and friend_pos != -1:
            return (total_cost, total_time, path)
        
        # Check if we've already visited this state with a better cost
        # A state is defined by (location, time)
        should_skip = False
        for time_entry, cost_entry in visited[current]:
            if time_entry == total_time and cost_entry <= total_cost:
                should_skip = True
                break
        
        if should_skip:
            continue
        
        # Add this state to visited
        # First remove any existing entry with the same time
        i = 0
        while i < len(visited[current]):
            if visited[current][i][0] == total_time:
                visited[current].pop(i)
            else:
                i += 1
        
        visited[current].append((total_time, total_cost))
        
        # Explore neighbors
        for neighbor, road_cost, road_time in graph[current]:
            new_cost = total_cost + road_cost
            new_time = total_time + road_time
            new_path = path + [neighbor]
            
            # Add to priority queue
            heapq.heappush(pq, (new_cost, new_time, neighbor, new_path))
    
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
    roads: List[Road] = [(0, 1, 10, 5), (1, 2, 5, 2), (2,0,35,4), (0,4,10,1), (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations: List[Station] = [(4, 3), (5, 2), (3, 4)]
    start: Location = 0
    friend_start: Location = 4
    result = intercept(roads, stations, start, friend_start)
    assert result == None, f'Expected None, got {result}'
    print("Test case 2 (unsolvable) passed.")
    
    # Test case 4, Same Cost, Different Time
    roads: List[Road] = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations: List[Station] = [(2,4), (1,3)]
    start: Location = 0
    friendStart: Location = 1
    result = intercept(roads, stations, start, friendStart)
    assert result == (10, 3, [0,2]), f'Expected (10, 3, [0,2]), got {result}'
    print("Test case 4 (same cost, different time) passed.")
    
    # Test case 3, Repeated locations
    roads: List[Road] = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations: List[Station] = [(4, 2), (5, 1), (3, 4)]
    start: Location = 0
    friend_start: Location = 3
    result = intercept(roads, stations, start, friend_start)
    assert result == (160, 39, [0,1,2,0,1,2,0,4]), f'Expected (160, 39, [0,1,2,0,1,2,0,4]), got {result}'
    print("Test case 3 (repeated locations) passed.")
    