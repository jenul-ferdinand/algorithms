from typing import List, Tuple
"""
Same as unbounded knapsack except that each item can only be picked at most once.

The difference is that if we pick an item X, giving us a remaining capacity R,
we have to somehow make sure that X is not part of the optimal solution to our
new subproblem of size R.
"""

def knapsack_01_bu(capacity, items):
    pass

def knapsack_01_td(capacity, items):
    pass

if __name__ == '__main__':
    # Example from the seminar
    capacity = 12
    items = [(9, 550), (5, 350), (6, 180), (1, 40)]
    res = knapsack_01_bu(capacity, items)
    exp = 780
    assert res == exp, f'Expected {exp}, got {res}'
    print(f'Passed!')