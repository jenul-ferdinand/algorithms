"""
? Name: 
Climbing Stairs

? Description:
You have a staircase with n steps.

Each move you can go up either 1 step or 2 steps.

Compute how many distinct ways there are to reach the top (step n)

? Approach
ways[i] = the number of distinct ways there are to reach the i-th 

Initially the number of ways to be at step 0 (starting point) is 1
And the number of ways to go to step 1 is 1 (0 -> 1)

To get to step 2 we can either go from step 0 -> 2 or 0 -> 1 -> 2, so the 
number of ways is 2

We can see that these subproblems can overlap, so we can reuse the result of 
the previous steps since we know that we can take one or two steps, we can take 
the result of the previous step and the one before that to get the number of 
ways for the current step.

? Reccurrence
ways[0] = 1
ways[1] = 1
ways[i] = ways[i - 1] + ways[i - 2] 
"""

def climb_stairs(num_stairs: int) -> int:
    """
    Finds the number of distinct ways to climb to a specific step. 
    
    Based on the rule that we can either take one step or two steps, going up.
    
    Time Complexity: O(n)
    Time Complexity Analysis:
        - We iterate through each step and calculate the number of ways to get
        to the current step in constant time. O(n) for doing this for all n 
        steps.
    
    Space Complexity: O(n)
    Space Complexity Analysis: 
        - Storing the `ways` array to store results: O(n)
    """
    def basic(num_stairs):
        n = num_stairs + 1
    
        ways = [None] * n
        ways[0] = 1 # Starting point (one way to stand at 0)
        ways[1] = 1 # First step (one way to get to step 1)
        
        for i in range(2, n):
            ways[i] = ways[i-1] + ways[i-2]
            
        return ways[num_stairs]
    
    def space_saving(num_stairs):
        """
        This one has:
        
        Space Complexity: O(1) because we only track three indices
        """
        n = num_stairs + 1
        ways = [None] * 3
        ways[0] = 1
        ways[1] = 1
        
        for _ in range(2, n):
            ways[2] = ways[1] + ways[0]
            
            # Update previous two
            ways[1], ways[0] = ways[2], ways[1]
            
        return ways[1]
    
    if basic(num_stairs) != space_saving(num_stairs): 
        return None
    
    return space_saving(num_stairs=num_stairs)
            
    

if __name__ == '__main__':
    # 4 Steps
    # The different ways to reach step 4:
    # 0 -> 1 -> 2 -> 3 -> 4
    # 0 -> 2 -> 3 -> 4
    # 0 -> 1 -> 2 -> 4
    # 0 -> 1 -> 3 -> 4
    # 0 -> 2 -> 4
    # So total 5 ways
    n = 4
    res = climb_stairs(n)
    exp = 5
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed')