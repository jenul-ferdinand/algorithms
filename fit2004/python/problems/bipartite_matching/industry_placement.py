"""
? Description
You are coordinating a industry placement unit.

There are a total of 240 students that are enrolled in the unit; and there are
30 companies to choose from:

- Each student is allowed to select 1 to 3 companies as their preferred 
placement, but they would only be placed in 1 company in the end.

- Each company would be able to accept 8 students.

- Students would reject any placements that is not in their preferred selection.

You realised that it is not possible for all students to be placed in their
preferred company as some companies are more popular than others. You would
however try to place as many students in their preferred companies as possible;
any students not placed in this round would be placed in the following round.

Describe how you would model this problem as a maximum flow problem which is 
then solved using the ford fulkerson method.
"""
from typing import List, Tuple, Dict, Optional
import networkx as nx

def industry_placement(
    prefs: Dict[int, List[int]], 
    num_companies: int,
    company_capacity: int = 8
):
    G = nx.DiGraph()
    s = 'source'
    t = 'sink'
    
    # Add edges source -> students (cap=1)
    for stu in prefs:
        G.add_edge(s, stu, capacity=1)
    
    # Add edges students -> companies (cap=1 with multiple edges for each pref)
    for stu, coms in prefs.items():
        for com in coms:
            G.add_edge(stu, f'company_{com}', capacity=1)
    
    # Add edges companies -> sink (cap=company capacity = 8)
    for com in range(1, num_companies + 1):
        G.add_edge(f'company_{com}', t, capacity=company_capacity)
    
    # Compute max flow
    flow_value, flow_dict = nx.maximum_flow(G, s, t)
    
    # Extract placements
    placements = {}
    for student in prefs:
        for com in prefs[student]:
            if flow_dict.get(student, {}).get(f'company_{com}', 0) == 1:
                placements[student] = com
                break
            
    return placements

if __name__ == '__main__':
    prefs = {
        1: [1,2,3],
        2: [2,4],
        3: [1,3,4],
        4: [1,2],
        5: [3,4]
    }
    num_companies = 4
    company_capacity = 8
    placements = industry_placement(prefs, num_companies, company_capacity)
    print("Industry placements:", placements)