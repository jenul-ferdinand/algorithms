from __future__ import annotations
from typing import TypeVar

from computer import Computer

T = TypeVar("T")

def binary_search(l: list[T], item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _binary_search_aux(l, item, 0, len(l))

def _binary_search_aux(l: list[T], item: T, lo: int, hi: int) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    if lo == hi:
        return lo
    mid = (hi + lo) // 2
    if l[mid] > item:
        # Item would be before mid
        return _binary_search_aux(l, item, lo, mid)
    elif l[mid] < item:
        # Item would be after mid
        return _binary_search_aux(l, item, mid+1, hi)
    elif l[mid] == item:
        return mid
    raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")

def new_binary_search(l: list[T], item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _new_binary_search_aux(l, item, 0, len(l))

def _new_binary_search_aux(l: list[Computer], item: Computer, lo: int, hi: int) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    if lo == hi:
        return lo

    mid = (hi + lo) // 2
    
    mid_item = (l[mid].hacking_difficulty, l[mid].risk_factor, l[mid].name)
    search_item = (item.hacking_difficulty, item.risk_factor, item.name)
    
    if mid_item > search_item:
        return _new_binary_search_aux(l, item, lo, mid)
    elif mid_item < search_item:
        return _new_binary_search_aux(l, item, mid + 1, hi)
    else:
        return mid
    
    raise ValueError(f'Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.')
