import sys
import os
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms_graph.ford_fulkerson import ford_fulkerson

# Type alias for an edge in the original graph with demand information
# (source_node, destination_node, capacity, demand)
OriginalEdgeWithDemand = Tuple[int, int, int, int]

# Type alias for an edge in the flow network for Ford-Fulkerson
# (source_node, destination_node, capacity)
FlowNetworkEdge = Tuple[int, int, int]

def is_feasible_circulation(
    num_original_vertices: int,
    edges_with_demand: List[OriginalEdgeWithDemand]
) -> bool:
    net_demands = [0] * num_original_vertices

    # Calculate net demand for each original vertex
    for u, v, capacity, demand in edges_with_demand:
        if demand > capacity:
            return False
        net_demands[u] -= demand # Demand leaving u
        net_demands[v] += demand # Demand entering v
        
    # Define super_source and super_sink for the Flow Network
    # Original vertices are 0 to num_original_vertices - 1
    # super_source will be num_original_vertices
    # super_sink will be num_original_vertices + 1
    super_source = num_original_vertices
    super_sink = num_original_vertices + 1
    num_flow_network_vertices = num_original_vertices + 2
    
    flow_edges: List[FlowNetworkEdge] = []
    total_demand_from_super_source = 0
    
    # Add edges from super_source to nodes with net positive demand
    # Add edges from nodes with net negative demand to super_sink
    for i in range(num_original_vertices):
        if net_demands[i] > 0:
            flow_edges.append((super_source, i, net_demands[i]))
            total_demand_from_super_source += net_demands[i]
        elif net_demands[i] < 0: 
            flow_edges.append((i, super_sink, -net_demands[i]))
    
    # Add original edges to the flow network with reduced capacities
    for u, v, capacity, demand in edges_with_demand:
        residual_capacity = capacity - demand
        if residual_capacity < 0:
            # This case should ideally be caught by the demand > capacity check
            # but as a safeguard for graph construction:
            return False
        if residual_capacity > 0:
            flow_edges.append((u, v, residual_capacity))
            
    if total_demand_from_super_source == 0:
        # If there's no net demand to be satisifed from super source,
        # and all demands are met by supplies (or demands are zero),
        # it's trivially feasible if all d <= c (checked).
        # This also handles the case where the graph is empty or has no demands.
        return True
    
    # Calculate the max flow in the constructed network
    max_flow = ford_fulkerson(
        num_flow_network_vertices, flow_edges, super_source, super_sink
    )
    
    # A feasible circulation exists if the max flow equals the total demand 
    # from the super source.
    # return int(max_flow) == total_demand_from_super_source
    return abs(max_flow - total_demand_from_super_source) < 1e-9 # Using tolerance for float 
        
if __name__ == '__main__':
    # Example 1: Trivial case, no edges, no demands
    num_nodes5 = 3
    edges5 = []
    print(f"Example 5 Feasible (no edges): {is_feasible_circulation(num_nodes5, edges5)}") # Expected: True
    
    # 
    num_nodes = 3
    edges = [
        (0, 1, 2, 2),
        (1, 2, 1, 2)
    ]
    print(f"Example 4 Not Feasible (flow cannot satisfy): {is_feasible_circulation(num_nodes, edges)}")
    
    
    num_nodes = 2
    edges = [(0, 1, 10, 5)]
    print(f'Feasible example last: {is_feasible_circulation(num_nodes, edges)}')