import sys
import os
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms_graph.ford_fulkerson import ford_fulkerson


BipartiteEdge = Tuple[int, int]
Edge = Tuple[int, int, int]

def max_bartite_matching(
    num_lhs: int, 
    num_rhs: int, 
    bipartite_edges: List[BipartiteEdge]
) -> int:
    """
    Calculates the maximum matching in a bipartite graph using FordFulkerson
    
    1. We create a super source node, which is then connected to the nodes in the 
    LHS of the bipartite graph. 
    
    2. We create a super sink node, connected from the nodes in the RHS of the 
    bipartite graph.
    
    Note that all edge connections have a capacity of 1, the we simply run
    ford fulkerson and output the result because max flow = max matchings.
    """
    super_source = 0
    super_sink = num_lhs + num_rhs + 1
    
    num_vertices = num_lhs + num_rhs + 2
    
    edges: List[Edge] = []
    
    # 1. Add edges from super source to all vertices in LHS
    for u_lhs in range(num_lhs):
        u = u_lhs + 1
        edges.append((super_source, u, 1))
        
    # 2. Add edges from all vertices in RHS to super sink 
    for v_rhs in range(num_rhs):
        v = num_lhs + v_rhs + 1
        edges.append((v, super_sink, 1))
        
    # 3. Add edges for the original bipartite connections (LHS to RHS)
    for u_lhs, v_rhs in bipartite_edges:
        u = u_lhs + 1
        v = num_lhs + v_rhs + 1
        edges.append((u, v, 1))
        
    # Calculate max flow using FordFulkerson
    return int(ford_fulkerson(num_vertices, edges, super_source, super_sink))


if __name__ == '__main__':
    # ? Example 1: A simple bipartite graph
    # LHS = {L0, L1, L2}, RHS = {R0, R1}
    # Edges = (L0, R0), (L0, R1), (L1, R0), (L2, R1)
    # Expected matching: 2
    num_lhs = 3
    num_rhs = 2
    edges = [
        (0,0),
        (0,1),
        (1,0),
        (2,1)
    ]
    max_matching = max_bartite_matching(num_lhs, num_rhs, edges)
    print(f'Example 1: Bipartite Graph with LHS={num_lhs}, RHS={num_rhs}')
    print(f'Edges: {edges}')
    print(f'Maximum Bipartite Matching size: {max_matching}') # Expected 2
    assert max_matching == 2, f'Test case 1 Failed: Expected 2, got {max_matching}'
    print('Test Case 1 Passed\n')