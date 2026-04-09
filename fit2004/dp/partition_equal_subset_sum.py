"""
? Name
Partition Equal Subset Sum

? Description
Given a non-empty list of positive integers `nums`. 

Determine if you can split the array into two subsets such that the sum of 
elements in both subsets is equal. 

Return True if such a partition exists, otherwise False.

This is a classic 0/1-knapsack style DP: you're effectively asking whether you
can pick a subset that sums to (total_sum // 2)
"""
from typing import List

def partition_equal_subset_sum(nums: List[int]) -> bool:
    n = len(nums)
    
    can_make = [[None] * n]
    

if __name__ == '__main__':
    # Test case
    # You can split as [1, 5, 5] and [11], both sum to 11 -> True
    nums = [1, 5, 11, 5]
    res = partition_equal_subset_sum(nums)
    exp = True
    print(f'Can {nums} be partitioned into equal-sum subsets? {res}')
    assert res == exp, f'Expected {exp}, got {res}'