from typing import List, Tuple
import heapq
import math

# Type aliases
Location = int # Location ID (non-negative integer)
Cost = int     # Cost of traveling on a road (+ve integer)
Time = int     # Time in minutes to travel on a road or train line

# A road is represented as a tuple of 
# (starting location, end location, cost of travel, time to travel)
Road = Tuple[Location, Location, Cost, Time] 

# A station is represented as a tuple of 
# (location of station, time it takes to travel to next location)
Station = Tuple[Location, Time]

# List of locations to form a route
Route = List[Location]

# A state is represented as a tuple of 
# (cost, time, location, remainder, path)
State = Tuple[Cost, Time, Location, Time, Route]

# Infinity constant value
INFINITY = math.inf

def intercept(
    roads: List[Road],       # Each road is a directed road
    stations: List[Station], # Can loop back to first station after last station
    start: Location, 
    friend_start: Location
) -> Tuple[Cost, Time, Route] | None:
    """
    Function description:
        Finds the optimal route for a driver to intercept their friend at a train
        station. Prioritising cost over time, meaning that if multiple routes share 
        the same cost, the one with the least total driving time will be chosen.
    
    Approach description (main function):

    
    1. First we determine the maximum number of locations in the graph. We do this
    by iterating through the roads start and end locations and finding the maximum.
    We also check the stations to find the maximum location, this is important,
    because one or more station(s) might not be connected to any roads locations.
    
    2. We create the adjacency list as a list of empty lists, where each entry
    will contain a tuple of (destination location, cost, time). The key will be 
    the starting location of the road (i.e. `graph[0]` to check location 0's
    neighbours).
    
    3. We find the index of the friend's starting station in the stations list.
    We do this by checking if any stations in the list match the friend's 
    starting location.
    
    4. We rearrange the stations list such that the friend's station will be the 
    first. This is important as the train will loop back to the first station 
    after the last. We want to follow where the friend is going.
    
    5. We compute the scheduled time for each station and the total loop time.
    This will store the exact times in the cycle when the friend arrives at each
    station. We also compute the maximum possible cycle time, this is used to
    determine the time when the train is at each station. 
    
    6. We initialise the state tracking for modified Dijkstra. This will store
    the best cost and time for each (location, time % cycle_time) pair.
    
    7. We initialise the MinHeap for modified Dijkstra. It holds:
    (total_cost, total_time, location, remainder, path). The MinHeap prioritises
    the lowest cost first, then the lowest time, other values in the tuple act
    as tie breakers.
    
    8. We start the main search loop for finding the optimal interception path.
    While there are states to explore in the MinHeap, we pop the current state
    from the MinHeap. If the current state has a better path compared to the
    current state, we skip it. We check if the current location is a station,
    if it is, we check if we arrive at the same time as the train. If we do,
    we return the (total_cost, total_time, path). if we don't, we explore the
    neighbours of the current location. We relax the state if the new state has
    a better path compared to the current state. We push the new state into the
    MinHeap. This continues until we find the optimal interception path or 
    exhaust all states in the MinHeap.
    
    Args:
        - roads: List of roads, each represented as a tuple (start, end, cost, time)
        - stations: List of stations, each represented as a tuple (location, time)
        - start: Starting location of the user
        - friend_start: Starting location of the friend
        
    Returns:
        - A tuple containing the total cost, total time, and the optimal route taken.
        - If no route is found, you'll get None. 
    
    Time Complexity: 
        - O(|R| log |L|) time.
        - |R| is the number of roads and |L| is the number of locations.
        
    Time Complexity Analysis:
        The algorithm uses a modified Dijkstra's algorithm to find the optimal
        interception path. The main loop runs while there are states in the MinHeap.
        Popping from the MinHeap takes O(log |L|) time, and exploring the neighbours
        takes O(|R|) time. The total time complexity is O(|R| log |L|) because we
        are using a MinHeap to keep track of the states. The number of states is 
        bounded by the number of roads and locations. The modified Dijkstra
        part dominates in time overall.
        
    Space Complexity:
        - O(|L| + |R|) auxiliary space.
        - |L| is the number of locations and |R| is the number of roads.
        
    Space Complexity Analysis:
        The algorithm uses a graph represented as an adjacency list, which takes
        O(|L| + |R|) space. The best_cost and best_time arrays also take 
        O(|L| * cycle_time) space. The MinHeap takes O(|L|) space. Overall, 
        the space complexity is O(|L| + |R|). Note that the worst case possible
        cycle time is 20 stations x 5 mins/journey = 100 minutes. This is a 
        constant value, so it doesn't affect the overall space complexity.
        
    Note for marker: 
        I have used a less pythonic style for this algorithm, hoping for better 
        readability and easier complexity analysis.
    """
    assert 2 <= len(stations) <= 20, f'No. of total stations |T| must be between 2 and 20 (inclusive), got {len(stations)}'
    
    #&.1 Determine maximum number of locations |L|
    max_location: Location = 0
    for road in roads: 
        max_location = max(max_location, road[0], road[1])
    for station in stations:
        max_location = max(max_location, station[0])
        assert 1 <= station[1] <= 5, f'Station travel time must be between 1 to 5 (inclusive), got {station[1]}'

    #&.2 Initialize adjacency list as a list of empty lists.
    graph: List[List[Tuple[Location, Cost, Time]]] = []
    for _ in range(max_location + 1):
        graph.append([])
    #&.2.1 Each entry will contain (destination, cost, time) tuples.
    for road_start, road_end, road_cost, road_time in roads:
        graph[road_start].append((road_end, road_cost, road_time))

    #&.3 Find the index of the friend's starting station.
    friend_start_index: Location = -1
    for index, (station_location, _) in enumerate(stations):
        if station_location == friend_start:
            friend_start_index = index
            break
    if friend_start_index == -1:
        return None # friend_start is not in the stations list
    
    #&.4 Rearrange stations list such that the friend's station will be the first
    stations: List[Station] = stations[friend_start_index:] + stations[:friend_start_index]
    
    #&.5 Compute scheduled time for each station and total loop time.
    # This will store the exact times in the cycle when the friend arrives at each station.
    train_schedule: List[Time] = [-1] * (max_location + 1)
    # The cycle time is the total time taken to complete the loop of stations.
    cycle_time: Time = 0
    for station, journey_time in stations:
        train_schedule[station] = cycle_time
        cycle_time += journey_time
    # If the cycle time is still 0, it means the stations are not valid.
    if cycle_time == 0:
        return None

    #&.6 Initialise state tracking for modified Dijkstra
    # This will store the best cost and time for each (location, time % cycle_time) pair.
    best_cost: List[List[Cost]] = [[INFINITY] * cycle_time for _ in range(max_location + 1)]
    best_time: List[List[Time]] = [[INFINITY] * cycle_time for _ in range(max_location + 1)]
    
    start_rem: Time = 0  # Driver starts at time 0. Remainder is 0.
    best_cost[start][start_rem] = 0
    best_time[start][start_rem] = 0
    
    #&.7 Initialise MinHeap with starting state for modified Dijkstra
    min_heap: List[State] = [(0, 0, start, start_rem, [start])]
    
    #&.8 Main search to find optimal intercept path and exploring neighbouring states
    while min_heap:
        #&.8.1 Pop the current state (minimum) from the MinHeap [ O(log|L|) ]
        total_cost, total_time, curr_loc, time_remainder, path = heapq.heappop(min_heap)
        
        # Skip this state, if a better path is found
        is_worse_cost: bool = total_cost > best_cost[curr_loc][time_remainder]
        is_same_cost: bool = total_cost == best_cost[curr_loc][time_remainder]
        is_worse_time: bool = total_time > best_time[curr_loc][time_remainder]
        if is_worse_cost or (is_same_cost and is_worse_time):
            continue
        
        #&.8.2 Check interception: using the precomputed train schedule.
        is_current_location_a_station: bool = train_schedule[curr_loc] != -1
        if is_current_location_a_station: 
            # Get the time when the train is at this station in the cycle
            train_time: Time = train_schedule[curr_loc]
            # If we arrive at the same time as the train
            if time_remainder == train_time:
                return (total_cost, total_time, path)
    
        #&.8.3 Explore neighbors [ O(|R|) ]
        if curr_loc <= max_location:
            for neighbour_loc, road_cost, road_travel_time in graph[curr_loc]:
                new_cost: Cost = total_cost + road_cost
                new_time: Time = total_time + road_travel_time
                new_rem: Time = new_time % cycle_time
                
                # Relax if new state has better path compared to current state
                is_better_cost: bool = new_cost < best_cost[neighbour_loc][new_rem]
                is_same_cost: bool = new_cost == best_cost[neighbour_loc][new_rem]
                is_better_time: bool = new_time < best_time[neighbour_loc][new_rem]
                if is_better_cost or (is_same_cost and is_better_time):
                    best_cost[neighbour_loc][new_rem] = new_cost
                    best_time[neighbour_loc][new_rem] = new_time
                    # TODO: Improve the path tracking logic, only construct the path when needed
                    new_path: Route = path + [neighbour_loc]
                    new_state: State = (new_cost, new_time, neighbour_loc, new_rem, new_path)
                    heapq.heappush(min_heap, new_state) # O(log|L|) to push

    # No interception possibilties found
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
    roads: List[Road] = [(0,1,5,1), (1,2,5,1), (2,3,5,1), (3,0,5,7)]
    stations: List[Station] = [(1,3), (3, 5)]
    start: Location = 0
    friend_start: Location = 1

    result = intercept(roads, stations, start, friend_start)
    assert result == (15, 3, [0,1,2,3]), f'Expected (15, 3, [0,1,2,3]), got {result}'
    print("Test (circular route) passed.")
    
    # Test no valid path
    roads: List[Road] = [(0,1,5,2), (1,2,5,3), (2,0,5,4)]
    stations: List[Station] = [(3,2), (4,3)]
    start: Location = 0
    friend_start: Location = 3
    
    result = intercept(roads, stations, start, friend_start)
    assert result == None, f'Expected None, got {result}'
    print("Test (no valid path) passed.")

