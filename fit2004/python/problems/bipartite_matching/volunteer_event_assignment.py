"""
? Name
Volunteer Event Assignment

? Description
You are organising a community festival with several simultaneous sessions 
(events). 

Each volunteer can sign up for up to 3 sessions they're interested in, but at
most one session will actually be assigned to them. 

Each session can only accomodate a fixed number of volunteers.

Your task is to assign as many volunteers as possible to one of their preffered
sessions, without ever exceeding any session's capacity.

? Approach
Create bipartite graph with volunteers on one side and sessions on the other.

Each volunteer can sign up to at most 3 sessions, so create edge with capacity
1 from VOLUNTEER ---> SESSION for each preferred session.

Create source node and connect to all volunteers with edge capacity of 1.
SOURCE ---> VOLUNTEERS

Create sink node and connect from all sessions with edge capacity of 
`session_capacity`, SESSIONS ---> SINK

Run max flow and get the assignments
"""
from typing import List, Dict
import networkx as nx

def assign_volunteers(
    preferences: Dict[int, List[int]],
    num_sessions: int,
    session_capacity: int = 4
) -> Dict[int, int]: 
    G = nx.DiGraph()
    source = 'src'
    sink = 'sink'
    
    # Add edges source -> volunteers (cap=1)
    for volunteer in preferences:
        G.add_edge(source, volunteer, capacity=1)
    
    # Add edges volunteer -> session (cap=1) for each preference
    for volunteer, sessions in preferences.items():
        for session in sessions:
            G.add_edge(volunteer, f'session_{session}', capacity=1)
            
    # Add edges session -> sink (cap=session_capacity) 
    for s in range(1, num_sessions + 1):
        G.add_edge(f'session_{s}', sink, capacity=session_capacity)
        
    # Compute max flow
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)
    
    # Extract assignments where flow_dict[volunteer][session] == 1
    assignments = {}
    for volunteer in preferences:
        for s in preferences[volunteer]:
            if flow_dict.get(volunteer, {}).get(f'session_{s}', 0) == 1:
                assignments[volunteer] = s
                break
            
    return assignments

if __name__ == '__main__':
    # Example: 5 volunteers, 4 sessions, each session holds at most 2 volunteers
    prefs = {
        101: [1,2,3],
        102: [2,4],
        103: [1,3,4],
        104: [1,2],
        105: [3,4]
    }
    num_sessions = 4
    session_capacity = 2
    
    assignments = assign_volunteers(prefs, num_sessions, session_capacity)
    print("Volunteer assignments:", assignments)