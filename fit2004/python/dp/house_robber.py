"""
? Name
House Robber

? Description
You are a professional house robber planning to rob houses along a street.

Each house has a non-negative amount of money stashed, given by a list nums.

Adjacent houses have security systems connected and will alert the police
if two adjacent houses are broken into on the same night.

Compute the maximum amount of money you can rob without ever robbing two 
adjacent houses.

rob[0] = nums[0]
rob[1] = max(nums[0], nums[1])
rob[i] = max(rob[i-1], rob[i-2] + nums[i])
"""
from typing import List

def house_robber(nums: List[int]) -> int:
    n = len(nums)
    
    if n == 0: return 0
    if n == 1: return nums[0]
    
    robbed = [None] * n
    robbed[0] = nums[0]
    robbed[1] = max(nums[0], nums[1])
    
    for i in range(2, n): 
        robbed[i] = max(robbed[i-1], robbed[i-2] + nums[i])
    
    return robbed[-1]

if __name__ == '__main__':
    # Main test
    nums = [2, 7, 9, 3, 1]
    # You cannot rob 7 and 3 together, so the optimal roberry is 2 + 9 + 1 = 12.
    res = house_robber(nums)
    exp = 12
    assert res == exp, f'Expected {exp}, got {res}'
    
    # Small case
    nums = [9]
    res = house_robber(nums)
    exp = 9
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')