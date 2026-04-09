from typing import List

def counting_sort(arr: List[int], u: int) -> List[int]:
    """
    Counting Sort
    
    Given that all elements in the input list are integers in [0, u-1], it:
        1. Counts the occurrences of each key.
        2. Computes prefix sums to determine the final index of each key.
        3. Builds a new output list by placing each element into its sorted
           position, iterating from right to left to ensure stability.
    
    Time Complexity: O(n + u)
    Time Complexity Analysis:
        - Counting occurrences -> O(n)
        - Computing prefix sums -> O(u)
        - Building the output array -> O(n)
        
    Auxiliary Space Complexity: O(n + u)
    Auxiliary Space Complexity Analysis:
        - `count` array of size u
        - `output` (new) list of size n
    """
    n = len(arr)
    
    # (1) Allocate the "count" array of size u, initialised to all zeros.
    count = [0] * u
    
    # (2) Count the occurrences of each key in arr.
    for x in arr:
        count[x] += 1
    
    # (3) Compute prefix sums so that count[i] is the number of elements <= i.
    for k in range(1, u):
        count[k] += count[k-1]
    
    # (4) Build the output list. Iterate from right -> left for stability.
    output = [0] * n
    for i in range(n-1, -1, -1):
        key = arr[i]
        count[key] -= 1
        position = count[key]
        output[position] = key
        
    return output


if __name__ == '__main__':
    arr = [4,2,1,3,2,0]
    res = counting_sort(arr, 5)
    exp = sorted(arr)
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')