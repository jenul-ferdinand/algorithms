"""
Write a python function where, given a sorted list of numbers, it asks for an
integer input and then returns true if the inputted integer exists in the list
and false otherwise.

Must run in O(logn) for lists that are already sorted (binary search)

"""


def _linear_search(arr: list, targ: int) -> bool:
    for i in arr:
        if i == targ:
            return True
    return False


def binary_search(arr: list, targ: int) -> bool:
    n = len(arr)

    lo = 0
    hi = n - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == targ:
            return True
        elif arr[mid] < targ:
            lo = mid + 1
        elif arr[mid] > targ:
            hi = mid - 1

    return False
