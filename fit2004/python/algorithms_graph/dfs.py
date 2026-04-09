def DFS(graph: dict[list[str]], node: str, visited=None, traversal=None) -> list:
    """
    Depth-first search algorithm
    
    Parameters:
        visited (set): a set of visited nodes
        graph (dict): a graph represented as a dictionary (adjacency list)
        node (str): the node to start the search from
        
    Time Complexity: 
        O(V + E), where V is the no. of vertices and E is the no. of edges
        
    Space Complexity:
        O(V), where V is the no. of vertices
    """
    if visited is None:
        visited = set()
    if traversal is None:
        traversal = []
        

    if node not in visited:
        visited.add(node)
        traversal.append(node)
        
        for neighbour in graph[node]:
            DFS(graph, neighbour, visited, traversal)
            
    return traversal

def DFS_iterative(graph: dict[list[str]], node: str, target: str) -> list:
    path = []
    stack = [node]
    
    while True:
        s = stack.pop()
        
        if s == target:
            path.append(s)
            return path
        
        if s not in path:
            path.append(s)
            
        if s not in graph:
            continue
        
        for neighbour in graph[s]:
            stack.append(neighbour)
        
    return path
        
            
            
if __name__ == '__main__':
    # Test graph
    graph = {
        '5': ['3', '7'],
        '3': ['2', '4'],
        '7': ['8'],
        '2': [],
        '4': ['8'],
        '8': []
    }
    
    result = DFS_iterative(graph, '5', '8')
    print(result)