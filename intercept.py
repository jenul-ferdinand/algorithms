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
        
        Determines the optimal route for a driver to intercept their friend at a
        train station. The optimal route minimises travel costs first, and then
        travel time as a tie-breaker. Interception requires arriving at a station
        at the exact same time as the friend's train. Uses Dijkstra on a 
        state-space graph with efficient path reconstruction using parent state
        tracking.
    
    Approach description (main function):
        Models the problem as a shortest path search on `(location, time_remainder)`
        state space. Pre-calculates the train schedule and cycle time. Uses
        Djikstra's algorithm with a MinHeap prioritised by (cost, time). Stores 
        the best cost, best time, and parent state `(prev_loc, prev_rem)` for
        each reachable state `(loc, rem)` in 2D lists. When an interception state
        is found, the path is reconstructed efficiently by backtracking through 
        the parent_info list. This avoids storing full paths in the heap.
    
    Input:
        - roads: List of roads, each represented as a tuple (start, end, cost, time)
        - stations: List of stations, each represented as a tuple (location, time)
        - start: Starting location of the user
        - friend_start: Starting location of the friend
        
    Output:
        - Tuple (total cost, total time, optimal route) if interception is possible.
        - If no route is found, you'll get None. 
    
    Time Complexity: O(|R| log |L|)
    Time Complexity Analysis:
        Dominated by Dijkstra with a MinHeap on the state space graph.
        Number of states O(|L| * C) = O(|L|). Number of edges O(|R| * C) = O(|R|).
        Heap operations take O(log |L|). Total time O(|R| log |L|).
        Path reconstruction takes O(P), where P is the path length (<= |L|*C = O(|L|)),
        which is less dominant than Dijkstra. Note that C is the cycle time, which is
        a constant value (<= 100 minutes max).
        
    Space Complexity: O(|L| + |R|) auxiliary space.
    Space Complexity Analysis:
        - Adjacency list `graph`: O(|L| + |R|) space.
        - `best_cost`, `best_time`: O(|L| * C) = O(|L|).
        - `parent_info`: O(|L| * C) = O(|L|). Stores tuples, constant size per entry.
        - MinHeap: Stores O(|L|) states, each constant size (no path list). O(|L|).
        - Reconstructed path: O(P) = O(|L|).
        Total auxiliary space: O(|L| + |R|)
        
    Terms:
        - |L|: Number of locations in the graph (including stations).
        - |R|: Number of roads in the graph.
        - C: Cycle time (total time taken to complete the loop of stations).
        - P: Number of locations in the optimal path.
        
    Note for marker: 
        I have used a less pythonic style for this algorithm, hoping for better 
        readability and easier complexity analysis. Also you can use the
        "Better Comments" VSCode extension to view comments as intended. 
        Thank you!
    """
    assert 2 <= len(stations) <= 20, f'No. of total stations |T| must be between 2 and 20 (inclusive), got {len(stations)}'
    
    #! Determine maximum number of locations |L|
    max_location: Location = 0
    for road in roads: 
        max_location = max(max_location, road[0], road[1])
    for station in stations:
        max_location = max(max_location, station[0])
        assert 1 <= station[1] <= 5, f'Station travel time must be between 1 to 5 (inclusive), got {station[1]}'

    #! Initialize adjacency list as a list of empty lists
    graph: List[List[Tuple[Location, Cost, Time]]] = []
    for _ in range(max_location + 1):
        graph.append([])
    # Each [starting location] entry will contain (destination, cost, time) tuples
    for road_start, road_end, road_cost, road_time in roads:
        graph[road_start].append((road_end, road_cost, road_time))

    #! Find the index of the friend's starting station
    friend_start_index: Location = -1
    for index, (station_location, _) in enumerate(stations):
        if station_location == friend_start:
            friend_start_index = index
            break
    if friend_start_index == -1:
        return None # friend_start is not in the stations list
    
    #! Rearrange stations list such that the friend's station will be the first
    stations: List[Station] = stations[friend_start_index:] + stations[:friend_start_index]
    
    #! Compute scheduled time for each station and total loop time
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

    #! Initialise state tracking for modified Dijkstra
    # This will store the best cost and time for each (location, cycle_time) pair.
    best_cost: List[List[Cost]] = [[INFINITY] * cycle_time for _ in range(max_location + 1)]
    best_time: List[List[Time]] = [[INFINITY] * cycle_time for _ in range(max_location + 1)]
    # Stores (parent_loc, parent_rem) for each (location, cycle_time) pair.
    parent_info: List[List] = [[None] * cycle_time for _ in range(max_location + 1)]
    
    # Initialise the starting state
    start_rem: Time = 0  # Driver starts at time 0. Remainder is 0.
    best_cost[start][start_rem] = 0
    best_time[start][start_rem] = 0
    
    #! Main search to find optimal intercept path and exploring neighbouring states
    # Initialise MinHeap with starting state (no need to heapify since just one)
    min_heap: List[State] = [(0, 0, start, start_rem)]
    while min_heap:
        #* Pop the current state (minimum) from the MinHeap [ O(log|L|) ]
        total_cost, total_time, curr_loc, time_remainder = heapq.heappop(min_heap)
        
        # Skip this state, if a better path is found
        is_worse_cost: bool = total_cost > best_cost[curr_loc][time_remainder]
        is_same_cost: bool = total_cost == best_cost[curr_loc][time_remainder]
        is_worse_time: bool = total_time > best_time[curr_loc][time_remainder]
        if is_worse_cost or (is_same_cost and is_worse_time):
            continue
        
        #* Check interception: using the precomputed train schedule.
        is_current_location_a_station: bool = train_schedule[curr_loc] != -1
        if is_current_location_a_station: 
            # Get the time when the train is at this station in the cycle
            train_time: Time = train_schedule[curr_loc]
            
            # If we arrive at the same time as the train
            if time_remainder == train_time:
                # Reconstruct the full path
                path = reconstruct_path(parent_info, start, curr_loc, time_remainder)
            
                return (total_cost, total_time, path)
    
        #* Explore neighbors [ O(|R|) ]
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

                    parent_info[neighbour_loc][new_rem] = (curr_loc, time_remainder)
                    
                    new_state: State = (new_cost, new_time, neighbour_loc, new_rem)
                    heapq.heappush(min_heap, new_state) # O(log|L|) to push

    # No interception possibilties found
    return None

def reconstruct_path(
    parent_info: List[List[Tuple[Location, Time]]],
    start_loc: Location,
    end_loc: Location,
    end_rem: Time
) -> Route:
    """
    Function Description:
        Helper function to reconstruct the path taken to intercept the friend.
        
    Approach Description:
        While the current location is not the starting location and the remainder
        is not 0 (indicating the end of the cycle), reconstruct the path backwards.
        The path is reconstructed by backtracking through the parent_info list.
        The path is built in reverse order, so it is reversed before returning.
    
    Input:
        - parent_info: 2D list where parent_info[loc][rem] stores the 
                       (prev_loc, prev_rem) tuple that led to state (loc, rem).
        - start_loc: Starting location of the entire journey
        - end_loc: The final location (interception station) of the path.
        - end_rem: The time remainder at the final location.
        
    Output:
        - A list of location IDs representing the path from start_loc to end_loc.
        
    Time Complexity: O(P), where P is the number of locations in the path.       
    Space Complexity: O(P), for storing the reconstructed path
    """
    route = []
    
    # Start from end location and remainder to backtrack until one before the start.
    current_loc: Location = end_loc
    current_rem: Time = end_rem
    
    # While the current location is not the starting location and the remainder is not 0
    # (indicating the end of the cycle), reconstruct the path backwards.
    while current_loc != start_loc or current_rem != 0:
        # Add the current location to the route
        route.append(current_loc)
        
        # Handle invalid current state
        is_curr_loc_invalid: bool = current_loc < 0 or current_loc >= len(parent_info)
        is_curr_rem_invalid: bool = current_rem < 0 or current_rem >= len(parent_info[current_loc])
        is_curr_state_none: bool = parent_info[current_loc][current_rem] == None
        if is_curr_loc_invalid or is_curr_rem_invalid or is_curr_state_none:
            return []
        
        # Get the previous state from current state
        prev_loc, prev_rem = parent_info[current_loc][current_rem]
        
        # Update the current state to the previous state
        current_loc, current_rem = prev_loc, prev_rem
    
    # Add the starting location
    route.append(start_loc)
    
    # Reverse the route and return it
    route.reverse() # In-place reversal!!!!!!
    return route

            

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

