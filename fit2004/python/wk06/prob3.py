from typing import List, Tuple
import heapq
from math import inf as INFINITY

"""
Consider the problem of planning a cross-country road trip. You have a map of 
Australia consisting of the locations of towns, each of which has a petrol 
station, with the corresponding petrol prices (which may be different at each 
town). You are currently at a particular town s and would like to travel to town 
t . Your car has a fuel capacity of C litres, and for each road on the map, you
know the amount of petrol it will take to travel along it. Your tank can only 
contain non-negative integer amounts of petrol, and all roads cost an integer 
amount of petrol to travel along. You cannot travel along a road if you do not
have enough petrol to make it all the way. You may refuel at any petrol station
whether your tank is empty or not (but only to integer values), and you are not 
required to fill your tank. Assuming that your tank is initially empty, describe
an algorithm for determining the cheapest way to travel to city t . [Hint: You
should model the problem as a shortest path problem and use Dijkstra's algorithm.]
"""

Location = int    # Location of a town
PetrolCost = int  # Petrol cost of a road
PetrolPrice = int # Petrol price of a town (to fill up the tank)
CurrentPetrol = int # Current petrol in the tank

# A town
Town = Tuple[Location, PetrolPrice]

# A road connecting two locations
Road = Tuple[Location, Location, PetrolCost]

# A state of being at a town with a certain amount of petrol in the tank
State = Tuple[PetrolCost, Location]

# A path from own town to another
Path = List[Location]

def plan(
    towns: List[Town],
    roads: List[Road],
    start: Location,
    end: Location
) -> Road:
    #! Get the max location
    for road in roads:
        max_location = max(max_location, road[0], road[1])
        
    #! Create the graph adjacency list
    graph = []
    for road in roads:
        u, v, cost = road[0], road[1], road[2]
        graph[u].append(v, cost)
        graph[v].append(u, cost)
        
    #! Create the visited list that stores the minimum cost to reach each town
    visited: List[PetrolCost] = [INFINITY * (max_location + 1)]
    # The best price to fill up the tank for each town
    best_price: List[PetrolPrice] = [INFINITY * (max_location + 1)]
    
    #! Set up initial state tracking
    # Cost of 0 to start at the starting town
    visited[start] = 0
    # Current petrol in the tank is 0
    capacity = 0
    # The best price to fill up the tank at the starting town
    best_price[start] = towns[start][1]
    
    #! Main search to find optimal path to the end town
    min_heap = [(0, start)]
    while min_heap:
        # Pop the minimum state from the heap
        cost, town = heapq.heappop(min_heap)
        
        # If we find the end town, return the cost
        if town == end:
            return cost
        
        # Check neighbours
        for neighbour, road_cost in graph[town]:
            new_cost: PetrolCost = cost + road_cost
            
            # Relax if new cost is less than the current cost
            is_better_cost: bool = new_cost < visited[neighbour]
            if is_better_cost:
                visited[neighbour] = new_cost
                
                new_state: State = (new_cost, neighbour)
                heapq.heappush(min_heap, new_state)
    

if __name__ == '__main__':
    pass