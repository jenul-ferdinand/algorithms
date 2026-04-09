
def find_threshold(max_height=150, prototypes=2):
    '''
    Determines the optimal strategy to find the threshold height x
    where a phone will break when dropped from heights > x.
    
    Returns the number of drops needed in the worst case.
    '''
    # For 2 prototypes, we use dynamic programming to find the answer.
    
    # drops[n][p] = min drops need for n floors with p prototypes
    drops = [[float('inf')] * (prototypes + 1) for _ in range(max_height + 1)]
    
    # Base cases
    # With 0 floors, we need 0 drops
    for p in range(prototypes + 1):
        drops[0][p] = 0
        
    # With 1 prototypes, we need exactly n drops for n floors
    for n in range(1, max_height + 1):
        drops[n][1] = n
        
    # Fill the table using optimal substructure
    for n in range(1, max_height + 1):
        for p in range(2, prototypes + 1):
            for f in range(1, n + 1):
                # Two cases:
                # 1. Phone breaks: We have (p-1) phones left for (f-1) floors below
                # 2. Phone survives: We have p phones left for (n-f) floors above
                drops[n][p] = min(
                    drops[n][p],
                    1 + max(drops[f-1][p-1], drops[n-f][p])
                )
                
    return drops[max_height][prototypes]
    
if __name__ == '__main__':
    result = find_threshold(150, 2)
    print(f'An optimal algorithm needs {result} drops in the worst case')