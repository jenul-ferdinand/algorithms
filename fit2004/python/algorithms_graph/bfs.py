from collections import deque # A better alterative to using list as queue

def BFS(graph: dict[list[str]], node: str, target: str) -> list[str]:
    """
    Breadth-first search algorithm
    
    Parameters:
        graph (dict): a graph represented as a dictionary (adjacency list)
        node (str): the starting node for the search
        target (str): the target node to find
    
    Time Complexity: 
        O(V + E), where V is the no. of vertices and E is the no. of edges.
    
    Space Complexity:
        O(V), where V is the no. of vertices.
    """
    visited = {}
    queue = deque()
    
    # Mark the starting node as visited and add it to the queue
    visited[node] = None
    # Add the starting node to the queue
    queue.append(node)
    
    # While there are nodes to process in the queue
    while queue:
        # Pop the first node from the queue
        m = queue.popleft()
        
        # If the node is the target, return the path
        if m == target:
            # Extract the path from the visited dictionary
            path = []
            while m:
                path.append(m)
                m = visited[m]
                
            return path[::-1] # Reverse the path to get the correct order
        
        # If the node is not the target, continue searching
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited[neighbour] = m
                queue.append(neighbour)
                

if __name__ == '__main__':
    test = {
        '5': ['3', '7'],
        '3': ['2', '4'],
        '7': ['8'],
        '2': [],
        '4': ['8'],
        '8': []
    }
    
    print(BFS(test, '5', '8'))