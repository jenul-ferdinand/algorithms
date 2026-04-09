from typing import List, Tuple, Set

"""
Given a capacity C and a set of items with their weights and values, you need
to pick items such that their total weight is at most C and their total value is
maximised. 

What is the maximum value you can take? 

In unbounded knapsack, you can pick an item as many times as you want.


Overlapping subproblems:
    memo[i] = LARGEST value with capacity at most i

Optimal substructure:
    max_value[C] = {
        if C < W_i for all i: 0
        else: max(v_i + max_value[C - W_i])
    }
    
Time complexity:
    O(NC)

Spacke complexity:
    O(C + N)
"""

Capacity = int
Weight = int
Value = int

def knapsack_unbounded_bu(capacity: Capacity, items: List[Tuple[Weight, Value]]):
    memo = [0] * (capacity + 1)
    
    for num in range(1, capacity + 1):
        max_value = 0
        for i in range(len(items)):
            weight = items[i][0]
            value = items[i][1]
            if weight <= num: 
                this_value = value + memo[num - weight]
                if this_value > max_value:
                    max_value = this_value
                    
        memo[num] = max_value
        
    return memo[capacity]

def knapsack_unbounded_td(capacity: Capacity, items: List[Tuple[Weight, Value]]):
    memo = [-1] * (capacity + 1)
    memo[0] = 0
    
    def knapsack_aux(capacity: Capacity):
        if memo[capacity] != -1:
            return memo[capacity]
        
        max_value = 0
        for i in range(len(items)):
            weight = items[i][0]
            value = items[i][1]
            if weight <= capacity:
                this_value = value + knapsack_aux(capacity - weight)
                if this_value > max_value:
                    max_value = this_value
                    
        memo[capacity] = max_value
        return memo[capacity]
    
    return knapsack_aux(capacity)
    

if __name__ == '__main__':
    # Example from the seminar
    # Testing bottom up
    print(f'Testing bottom up')
    capacity = 12
    items = [(9, 550), (5, 350), (6, 180), (1, 40)]
    result_bu = knapsack_unbounded_bu(capacity, items)
    answer = 780
    assert result_bu == answer, f'Expected {answer}, got {result_bu}'
    print(f'Passed!')
    # Testing top down
    print(f'Testing top down')
    capacity = 12
    items = [(9, 550), (5, 350), (6, 180), (1, 40)]
    result_td = knapsack_unbounded_td(capacity, items)
    answer = 780
    assert result_td == answer, f'Expected {answer}, got {result_td}'
    print(f'Passed!')
    
    # Example from preparation sheet
    capacity = 8
    items = [(2, 120), (3, 200), (5, 250), (7, 450), (10, 750)]
    print(knapsack_unbounded_bu(capacity, items))
    print(knapsack_unbounded_td(capacity, items))