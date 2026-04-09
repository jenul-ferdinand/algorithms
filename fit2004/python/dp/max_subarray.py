"""
? Name
Maximum Subarray

? Description
Given an integer array `nums`.

Find the contiguous subarray (containing at least one number)

dp[i] = what's the maximum subarray sum ending at index i for each i.

let dp[i] = max sum of subarary that ends exactly at i

dp[i] = max(dp[i-1] + nums[i], nums[i])
"""
from typing import List

def max_subarray(nums: List[int]) -> int:
    n = len(nums)
    
    dp = [0] * n
    dp[0] = nums[0]
    
    for i in range(n):
        dp[i] = max(dp[i-1] + nums[i], nums[i])
        
    return max(dp)

if __name__ == '__main__':
    # Test 1
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    # The contiguous subarray [4, -1, 2, 1] has the largest sum = 6
    res = max_subarray(nums)
    exp = 6
    print(f"Max subarray sum for {nums}: {res}")
    assert res == exp, f"Expected {exp}, got {res}"