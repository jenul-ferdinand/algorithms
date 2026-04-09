"""
? Description
You are coordinating a final year project unit.

There are a total of 123 students that are enrolled into the unit.
And there are 24 topics to choose from:

- Each student is allowed to select up to 4 preferred topics, 
  but they would only be assigned only to 1 topic at the end.
  
- Each topic can only be assigned to at most 5 students.

You realised that it is not possible for all students to be doing their
preferred topics, as some topics are more popular than others. You would
however prioritise to satisfy the preferences of as many students as possible.

Describe how you would model this problem as a maximum flow problem; which
is then solved using the Ford-Fulkerson method.

? Approach
This problem can be solved using standard bipartite matching using 
Ford-Fulkerson.

1. We have the 123 students each as nodes on the LHS.

2. We have he 24 topics on the RHS.

3. Add a source node on the LHS of the students.

4. Add a sink node on the RHS of the topics.

STUDENTS -> TOPICS
For each student node we create an outgoing edge to each of their preferred 
topics, with an edge capacity of 1.

SOURCE -> STUDENTS
Connect directed edges from the singular source node to all student nodes, with
an edge capacity of 1, this represents the fact that students can only be 
assigned to 1 topic.

TOPICS -> SINK
Connect directed edges from all of the topic nodes to the singular sink node, 
with an edge capacity of 5, this represents that each topic can only be assigned
to at most 5 students.

Run Ford-Fulkerson to find out the most optimal matching for this. This is 
based on the fact that when given integer capacity values, ford fulkerson will
return an integer valued flow. Running this will ensure that we will get an
optimal matching to maximise student satisfaction.
"""
from typing import List, Tuple, Dict
import networkx as nx

def assign_topics(
    preferences: Dict[int, List[int]],
    num_topics: int,
    topic_capacity: int = 5
) -> Dict[int, int]:
    """
    Build a flow network using NetworkX and compute a max-flow to assign each
    student to at most one of their preferred topics, with each topic having
    capacity `topic_capacity`.
    
    Args:
        preferences: Mapping from student_id -> list of preferred topic_ids
        num_topics: Total number of topics (topic_ids are assumed 1..num_topics)
        topic_capacity: Max students per topic
        
    Returns:
        A dict student_id -> assigned_topic_id for all assigned students.
        Students who could not be assigned (due to capacity limits) are omitted.
        
    Time Complexity: O((S + T) * (S + P + T)^2)
    Time Complexity Analysis:
        Let S = number of students
        Let T = number of topics
        Let P = total student-topic preference edges
        Then |V| = S + T + 2
        And  |E| = S (src -> students) + P (student -> topic) + T (topic -> sink)
                 = O(S + P + T)
                 
        NetworkX's default max-flow (Edmonds-Karp) runs in O(V * E^2) time.
    
    Auxiliary Space Complexity: O(V + E)
        - Storing the directed garph and residual capacities: O(V + E)
        - BFS queue, visited flags, and flow dictionaries: O(V + E)
    """
    G = nx.DiGraph()
    source = 'src'
    sink = 'sink'
    
    # Add edges source -> student (cap=1)
    for student in preferences:
        G.add_edge(source, student, capacity=1)
    
    # Add edges student -> topic (cap=1) for each preference
    for student, tops in preferences.items():
        for t in tops:
            G.add_edge(student, f'topic_{t}', capacity=1)
        
    # Add edges topic -> sink (cap=topic_capacity)
    for t in range(1, num_topics + 1):
        G.add_edge(f'topic_{t}', sink, capacity=topic_capacity)
        
    # Compute max flow
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)
    
    # Extract assignments where flow_dict[student][topic] == 1
    assignments = {}
    for student in preferences:
        for t in preferences[student]:
            if flow_dict.get(student, {}).get(f'topic_{t}', 0) == 1:
                assignments[student] = t
                break
            
    return assignments


if __name__ == '__main__':
    # Small test: 4 students, 3 topics, capacity 2 each
    prefs = {
        1: [1,2],
        2: [1,3],
        3: [1,2,3],
        4: [2,3]
    }
    n = 3
    tc = 2
    assigned = assign_topics(prefs, n, tc)
    print('Assignments:', assigned)



