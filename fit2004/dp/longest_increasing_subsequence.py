from typing import List

"""

A subsequence is an increasing order of numbers given some list of ints.

E.g.
- [3, 1, 8, 2, 5]
- The longest increasing subsequence here is [1, 2, 5]
- So the returned length should be 3

So we know that all increasing subsequences are subsets of the original sequence.

All increasing subsequences have a `start` and `end`.

Let's focus on the `end` index of an increasing subsequence.



? Overlapping subproblems:
- LIS[k] = LIS ending at k.
- Where LIS means Longest Increasing Sub-Sequence

So for seq = [3,1,8,2,5] => LIS[3] = 2 
              0 1 2 3 4
- This means the longest increasing sub-sequence ending at seq[3] which is 2.
- Has a length of 2 because we have the sub-sequence 1 -> 2

How do we use these subproblems to solve LIS[4]?
- LIS[0] = length 1 (just 3)
- LIS[1] = length 1 (3 -> 1 does not work)
- LIS[2] = length 2 (has sub-sequence 1 -> 8)
- LIS[3] = length 2 (has sub-sequences 1 -> 8 AND 1 -> 2)
- LIS[4] = 1 + max(LIS[0], LIS[1], LIS[2], LIS[3])

? Optimal substructure:
LIS[n] = 1 + max(LIS[k] such that k < n and arr[k] < arr[n])
"""

def longest_increasing_subsequence(arr: List[int]) -> int:
    """
    Finds the length of the longest subsequence in the given sequence.
    
    Time Complexity: O(n * s) = O(n^2) when s = Θ(n)
    - O(n) time for iterating through the sequence.
    - O(s) time for getting each subproblems
    
    Terms: 
    - n: length of the given sequence i.e., `arr`.
    """
    # All lengths are 1 by default
    LIS = [1] * len(arr)
    
    for i in range(len(arr)):
        # Optimal substructure
        subproblems = [LIS[k] for k in range(i) if arr[k] < arr[i]]
        
        # Specify the length for this index
        LIS[i] = 1 + max(subproblems, default=0)
    
    # Return the largest length we've found
    return max(LIS, default=0)

if __name__ == '__main__':
    arr = [3,1,8,2,5]
    res = longest_increasing_subsequence(arr)
    assert res == 3, f'Expected 3, got {res}'
    
    print('Test cases passed')
