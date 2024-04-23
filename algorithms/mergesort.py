from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")

def merge(l1: list[T], l2: list[T], key=lambda x:x) -> list[T]:
    """
    Merges two sorted lists into one larger sorted list,
    containing all elements from the smaller lists.

    The `key` kwarg allows you to define a custom sorting order.

    :pre: Both l1 and l2 are sorted, and contain comparable elements.
    :complexity: Best/Worst Case O(n * comp(T)), n = len(l1)+len(l2)
    :returns: The sorted list.
    """
    new_list = []
    cur_left = 0
    cur_right = 0
    while cur_left < len(l1) and cur_right < len(l2):
        if key(l1[cur_left]) <= key(l2[cur_right]):
            new_list.append(l1[cur_left])
            cur_left += 1
        else:
            new_list.append(l2[cur_right])
            cur_right += 1
    new_list += l1[cur_left:]
    new_list += l2[cur_right:]
    return new_list

def mergesort(l: list[T], key=lambda x:x) -> list[T]:
    """
    Sort a list using the mergesort operation.
    :complexity: Best/Worst Case O(NlogN * comp(T))
    """
    if len(l) <= 1:
        return l
    break_index = (len(l)+1) // 2
    l1 = mergesort(l[:break_index], key=key)
    l2 = mergesort(l[break_index:], key=key)
    return merge(l1, l2, key=key)

def new_merge(l1: list[T], l2: list[T], hacking_diff = lambda x : x.hacking_difficulty, risk_factor = lambda x : x.risk_factor, name = lambda x : x.name) -> list[T]:
    new_list = []
    cur_left = 0
    cur_right = 0
    while cur_left < len(l1) and cur_right < len(l2):
        comp1 = (hacking_diff(l1[cur_left]), risk_factor(l1[cur_left]), name(l1[cur_left]))
        comp2 = (hacking_diff(l2[cur_right]), risk_factor(l2[cur_right]), name(l2[cur_right]))
        if comp1 < comp2:
            new_list.append(l1[cur_left])
            cur_left += 1
        else:
            new_list.append(l2[cur_right])
            cur_right += 1
    new_list += l1[cur_left:]
    new_list += l2[cur_right:]
    return new_list

def new_mergesort(l: list[T], hd = lambda x : x.hacking_difficulty, rf=lambda x: x.risk_factor, n=lambda x: x.name) -> list[T]:
    if len(l) <= 1:
        return l
    break_index = (len(l)+1) // 2
    l1 = new_mergesort(l[:break_index], hd=hd, rf=rf, n=n)
    l2 = new_mergesort(l[break_index:], hd=hd, rf=rf, n=n)
    return new_merge(l1, l2, hacking_diff=hd, risk_factor=rf, name=n)

