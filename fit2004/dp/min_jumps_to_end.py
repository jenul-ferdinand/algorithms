"""
? Name
Minumum Jumps to Reach End

? Description:
Given an array nums of non-negative integers where nums[i] is the maximum jump 
length you can make from index i.

return the minimum number of jumps needed to reach the last index. 

You may assume you can always reach the end.

This is a 1D DP (or greedy) problem: at each position, you decide how far to
jump next to minimise the total jumps.

& Subproblems
Let dp[i] = "minimum jumps needed to reach index i"
dp[0] = 0 because we start there.

& Transitions
To get dp[i], ask: "What could have been my previous position j, so that from
j I can jump to i?"
The condition is j + nums[j] >= i (i.e., j's max-jump reaches or passes i)

Among all such j < i, we pick the one with the smallest dp[j] then add 1 jump.
dp[i] = 1 + min{dp[i] | 0 <= j < i and j + nums[j] >= i}
"""
from typing import List

def min_jumps(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1: return 0
    
    dp = [None] * n
    dp[0] = 0
    
    for i in range(1, n):
        candidates = [
            dp[j]
            for j in range(i)
            if dp[j] is not None and j + nums[j] >= i
        ]
        if candidates:
            dp[i] = 1 + min(candidates)
                
    return dp[-1]

if __name__ == '__main__':
    # Test 1
    nums = [2,3,1,1,4] 
    # Optimal path: 0 -> 1 -> 4 or 0 -> 2 -> 4, both take two jumps.
    res = min_jumps(nums)
    exp = 2
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')