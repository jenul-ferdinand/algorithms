"""
Problem 2. Devise an algorithm that, given a box with n different locks and n 
corresponding keys, matches the keys and locks in average-case time complexity 
O (n log n). Each lock matches only one key, and each key matches only one lock.
You can try a key in a lock to determine whether the key is larger than, smaller 
than or fits the lock. However, you cannot compare two keys or two locks 
directly.
"""
import random
from typing import List, Tuple, Callable, TypeVar, Dict

K = TypeVar('K')
L = TypeVar('L')

def match_keys_and_locks(
    keys: List[K],
    locks: List[L],
    compare: Callable[[K, L], int]
) -> Dict[K, L]:
    """
    Match each key to its corresponding lock using only cross comparisons.
    
    Average Time Complexity: O(n log n)
        - Each recursive partition step processes O(n) items.
        - Pivot choice is random => average recursion depth O(log n)
    
    Auxiliary Space Complexity: O(n)
        - For recursion stack and temporary lists.
    """
    if not keys:
        return {}
    
    # 1. Pick a random pivot lock
    pivot_lock = random.choice(locks)
    
    # 2. Partition keys around pivot_lock
    lt_keys, eq_keys, gt_keys = [], [], []
    for k in keys:
        c = compare(k, pivot_lock)
        if c < 0:
            lt_keys.append(k)
        if c == 0:
            eq_keys.append(k)
        if c > 0:
            gt_keys.append(k)
            
    # There must be exactly one matching key
    pivot_key = eq_keys[0]
    
    # 3. Partition locks aruond pivot_key
    lt_locks, eq_locks, gt_locks = [], [], []
    for l in locks:
        c = compare(pivot_key, l)
        if c < 0:
            gt_locks.append(l)
        if c == 0:
            eq_locks.append(l)
        if c > 0:
            lt_locks.append(l)
            
    # 4. Recurse on partitions
    result = {}
    result.update(match_keys_and_locks(lt_keys, lt_locks, compare))
    result[pivot_key] = pivot_lock
    result.update(match_keys_and_locks(gt_keys, gt_locks, compare))
    return result

if __name__ == '__main__':
    # Test with integer keys and locks; compare by numeric order
    keys = [5, 1, 4, 2, 3]
    locks = [3, 5, 1, 2, 4]

    def cmp_int(k: int, l: int) -> int:
        return (k > l) - (k < l)

    matches = match_keys_and_locks(keys, locks, cmp_int)
    # Expect each key maps to itself
    for k in keys:
        assert matches[k] == k, f"Key {k} should match lock {k}, got {matches[k]}"
    print("All key-lock matches correct!")