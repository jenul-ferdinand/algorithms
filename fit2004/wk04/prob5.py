"""
A subroutine used by QuickSort is the partitioning function which takes a list
and rearranges the elements such that all elements <= p come before all elements
> p where p is the pivot element. 

Suppose one instead has k <= n pivot elements and wishes to rearrange the list
such that all elements <= p_1 come before all elements that are > p_1 and < p_2 
and so on..., where p_1, p_2, ..., p_k denote the pivots in sorted order. The 
pivots are not necessarily given in sorted order in the input.

(a) Write an algorithm for performing k-partitioning in O(nk) time. 

(b) Write a better algorithm for performing k-partitioning in O(nlogk) time.

(c) Is it possible to write an algorithm for k-partitioning that runs faster
than O(nlogk)?

"""
from typing import List, TypeVar
import bisect

T = TypeVar('T')



def k_partition_naive(A: List[T], pivots: List[T]) -> List[T]:
    """
    Partition a list A into k+1 regions defined by k pivot values.
    """
    # 1. Sort the pivots
    sorted_pivots = sorted(pivots)
    k = len(sorted_pivots)
    
    # 2. Create k+1 empty buckets
    buckets = [[] for _ in range(k+1)]
    
    # 3. Assign each element of A to the appropriate bucket
    for x in A:
        placed = False
        for i, pivot in enumerate(sorted_pivots):
            if x <= pivot:
                buckets[i].append(x)
                placed = True
                break
            
        if not placed:
            buckets[k].append(x)
            
    # 4. Concatenate all buckets in order
    result = []
    for bucket in buckets:
        result.extend(bucket)
        
    return result



def k_partition_binary_search(A: List[T], pivots: List[T]) -> List[T]:
    """
    Partition a list A into k+1 regions defined by k pivot values in 
    O(k log k + n log k) time by sorting pivots once and then using binary
    search per element.
    
    """
    # 1. Sort the pivots
    pivots = sorted(pivots)
    
    # 2. Create k+1 buckets
    buckets = [[] for _ in range(len(pivots) + 1)]
    
    # 3. Assigne each element of A to the correct bucket via bisect_left
    for x in A:
        idx = bisect.bisect_left(pivots, x)
        buckets[idx].append(x)
        
        
    # 4. Flatten buckets into one list
    result = []
    for b in buckets:
        result.extend(b)
    return result



if __name__ == '__main__':
    # Test case 1: example from description
    A = [7, 2, 5, 3, 9, 1, 4, 8, 6]
    pivots = [3, 6]
    # Regions: ≤3 → [2,3,1], (3,6] → [5,4,6], >6 → [7,9,8]
    out = k_partition_naive(A, pivots)
    exp = [2, 3, 1, 5, 4, 6, 7, 9, 8]
    assert out == exp, f"Test1: expected {exp}, got {out}"

    # Test case 2: single pivot, unsorted input
    A = [5, 1, 4, 2, 3]
    pivots = [3]
    # Regions: ≤3 → [1,2,3], >3 → [5,4]
    out = k_partition_naive(A, pivots)
    exp = [1, 2, 3, 5, 4]
    assert out == exp, f"Test2: expected {exp}, got {out}"

    # Test case 3: no pivots → output == input
    A = [10, 9, 8, 7]
    pivots = []
    out = k_partition_naive(A, pivots)
    exp = [10, 9, 8, 7]
    assert out == exp, f"Test3: expected {exp}, got {out}"

    # Test case 4: pivots unsorted, repeated values
    A = [4, 2, 4, 1, 3, 5]
    pivots = [3, 2, 4]
    # sorted_pivots = [2,3,4]
    # Regions: ≤2→[2,1], (2,3]→[3], (3,4]→[4,4], >4→[5]
    out = k_partition_naive(A, pivots)
    exp = [2, 1, 3, 4, 4, 5]
    assert out == exp, f"Test4: expected {exp}, got {out}"

    print("All naive k-partition tests passed!")
    
    
    
    # Test case 1: two pivots
    A = [7, 2, 5, 3, 9, 1, 4, 8, 6]
    pivots = [3, 6]
    # Regions: ≤3 → [2,3,1], (3,6] → [5,4,6], >6 → [7,9,8]
    out = k_partition_binary_search(A, pivots)
    exp = [2, 3, 1, 5, 4, 6, 7, 9, 8]
    assert out == exp, f"Test1 failed: expected {exp}, got {out}"

    # Test case 2: single pivot
    A = [5, 1, 4, 2, 3]
    pivots = [3]
    # Regions: ≤3 → [1,2,3], >3 → [5,4]
    out = k_partition_binary_search(A, pivots)
    exp = [1, 2, 3, 5, 4]
    assert out == exp, f"Test2 failed: expected {exp}, got {out}"

    # Test case 3: no pivots (k=0)
    A = [10, 9, 8, 7]
    pivots = []
    out = k_partition_binary_search(A, pivots)
    exp = [10, 9, 8, 7]
    assert out == exp, f"Test3 failed: expected {exp}, got {out}"

    # Test case 4: unsorted and repeated pivots
    A = [4, 2, 4, 1, 3, 5]
    pivots = [4, 2, 3]
    # sorted_pivots = [2,3,4]
    # Regions: ≤2→[2,1], (2,3]→[3], (3,4]→[4,4], >4→[5]
    out = k_partition_binary_search(A, pivots)
    exp = [2, 1, 3, 4, 4, 5]
    assert out == exp, f"Test4 failed: expected {exp}, got {out}"

    # Test case 5: all elements equal
    A = [1, 1, 1, 1]
    pivots = [1, 1]
    # Regions: ≤1→all, the rest empty
    out = k_partition_binary_search(A, pivots)
    exp = [1, 1, 1, 1]
    assert out == exp, f"Test5 failed: expected {exp}, got {out}"

    print("All binary‐search k‐partition tests passed!")