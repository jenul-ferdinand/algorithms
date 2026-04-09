import sys
import os
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms_graph.ford_fulkerson import ford_fulkerson

"""
Problem 4. 
Consider the problem of allocating a set of jobs to one of two 
supercomputers. Each job must be allocated to exactly one of the two computers.
The two computers are configured slightly differently, so for each job, you know
how much it will cost on each of the computers. There is an additional 
constraint. Some of the jobs are related, and it would be preferable, but not
required, to run them on the same computer. For each pair of related jobs, you
know how much more it will cost if they are run on separate computers. Give an
efficient algorithm for determining the optimal way to allocate the jobs to the
computers, where your goal is to minimise the total cost.

* A set of jobs must be allocated to one of two computers.

* Each job must be allocated to exactly one of the two computers.

* T
"""

JobID = int
Cost = int
# (from_node, to_node, capacity)
FlowEdge = Tuple[int, int, int]
# (job1_id, job2_id, penalty_cost)
RelatedPairPenalty = Tuple[JobID, JobID, Cost]

def optimal_job_allocation(
    num_jobs: int, 
    costs_computer1: List[Cost], 
    costs_computer2: List[Cost],
    related_jobs_penalties: List[RelatedPairPenalty]
) -> Cost:
    source_node = 0
    
    sink_node = num_jobs + 1
    num_total_vertices = num_jobs + 2
    
    flow_network_edges: List[FlowEdge] = []
    
    # 2. Add edges for individual job costs
    for j in range(num_jobs):
        jobs_node_idx = j + 1
        
        # Edge from Source to Job_j
        cost_j_to_c2 = costs_computer2[j]
        flow_network_edges.append((source_node, jobs_node_idx, cost_j_to_c2))
        
        # Edge from Job_j to Sink
        cost_j_on_c1 = costs_computer1[j]
        flow_network_edges.append((jobs_node_idx, sink_node, cost_j_on_c1))
    
    # 3. Add edges for related job penalties
    for job_i, job_j, penalty in related_jobs_penalties:
        j_node_idx = job_i + 1
        i_node_idx = job_j + 1
        
        flow_network_edges.append((i_node_idx, j_node_idx, penalty))
        flow_network_edges.append((j_node_idx, i_node_idx, penalty))
        
    # 4. Calculate the max flow (which equals min cut)
    min_total_cost = ford_fulkerson(
        num_total_vertices,
        flow_network_edges,
        source_node,
        sink_node
    )
    
    return int(min_total_cost) 

if __name__ == '__main__':
    # Example Test Case (You'll need to create some)
    # Let's define a simple scenario:
    # 2 jobs (Job 0, Job 1)
    
    # Costs:
    # Job 0: C1=10, C2=5
    # Job 1: C1=6, C2=12
    num_jobs_ex1 = 2
    costs_c1_ex1 = [10, 6]  # Cost of Job 0 on C1, Job 1 on C1
    costs_c2_ex1 = [5, 12] # Cost of Job 0 on C2, Job 1 on C2
    
    # Related jobs:
    # Job 0 and Job 1 are related with a penalty of 3 if separated.
    related_ex1 = [(0, 1, 3)] # (job_id_1, job_id_2, penalty)

    min_cost_ex1 = optimal_job_allocation(num_jobs_ex1, costs_c1_ex1, costs_c2_ex1, related_ex1)
    print(f"Example 1: Minimum allocation cost: {min_cost_ex1}")

    # Expected analysis for Example 1:
    # Nodes: S=0, J0=1, J1=2, T=3
    # Edges from S: (0,1, cap=5), (0,2, cap=12)
    # Edges to T:   (1,3, cap=10), (2,3, cap=6)
    # Penalty edges:(1,2, cap=3), (2,1, cap=3)

    # Possible allocations and their costs:
    # 1. J0 on C1, J1 on C1:
    #    Cost = Cost(J0,C1) + Cost(J1,C1) = 10 + 6 = 16
    #    Cut: (J0,T), (J1,T) -> Edges (1,3) and (2,3) cut. Capacity = 10 + 6 = 16.
    #
    # 2. J0 on C2, J1 on C2:
    #    Cost = Cost(J0,C2) + Cost(J1,C2) = 5 + 12 = 17
    #    Cut: (S,J0), (S,J1) -> Edges (0,1) and (0,2) cut. Capacity = 5 + 12 = 17.
    #
    # 3. J0 on C1, J1 on C2: (Separated)
    #    Cost = Cost(J0,C1) + Cost(J1,C2) + Penalty(J0,J1) = 10 + 12 + 3 = 25
    #    Cut: (J0,T), (S,J1), (J0,J1) -> Edges (1,3), (0,2), (1,2) cut. Capacity = 10 + 12 + 3 = 25.
    #
    # 4. J0 on C2, J1 on C1: (Separated)
    #    Cost = Cost(J0,C2) + Cost(J1,C1) + Penalty(J0,J1) = 5 + 6 + 3 = 14
    #    Cut: (S,J0), (J1,T), (J1,J0) -> Edges (0,1), (2,3), (2,1) cut. Capacity = 5 + 6 + 3 = 14.
    #
    # So, for this example, the minimum cost should be 14.
    assert min_cost_ex1 == 14, f"Test Case 1 Failed: Expected 14, got {min_cost_ex1}"
    print("Test Case 1 Passed!")

    # Example 2: No related jobs
    num_jobs_ex2 = 2
    costs_c1_ex2 = [10, 100]
    costs_c2_ex2 = [50, 5]
    related_ex2 = []
    min_cost_ex2 = optimal_job_allocation(num_jobs_ex2, costs_c1_ex2, costs_c2_ex2, related_ex2)
    print(f"Example 2: Minimum allocation cost: {min_cost_ex2}")
    # J0: C1=10, C2=50 -> Choose C1 (cost 10)
    # J1: C1=100, C2=5 -> Choose C2 (cost 5)
    # Total = 10 + 5 = 15
    assert min_cost_ex2 == 15, f"Test Case 2 Failed: Expected 15, got {min_cost_ex2}"
    print("Test Case 2 Passed!")