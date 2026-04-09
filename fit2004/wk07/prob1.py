"""
* selling n houses along a street.

* we already workout the amount we get from selling each house.
- the element in the houses list is the profit we get from each house

* We can't sell houses right next to each other.

* We have to select a subset of houses such that we make the most amount of money.

starting with the i-th house what are my actions?

1. Sell to this house: Get profit for this house, but then you cannot sell to adjacent houses.
    - profit from houses[0 .. i-2] + sale of houses[i]

2. Skip this house: Get no profit from this house, but you keep your options open for adjacent houses.
    - skip house i and take max profit from houses [0 .. i - 1]
    - profit from houses[0 .. i-1]

Base cases:
- What's the maximum profit for just house 0?
    - profit = house[0]
    
- What's the maximum profit when considering only houses 0 and 1?
    - profit = max(house[0], house[1])

Optimal substructure:
    memo[0] = houses[0]
    memo[1] = max(houses[0], houses[1])
    memo[i] = max(houses[i] + memo[i-2], memo[i-1]) for i >= 2
    
Overlapping sub problems:
    - Initially we have the base cases memo[0] and memo[1]
    - For i >= 2, we use those previous base cases in our optimal substructure
        - memo[i] = max(houses[i] + memo[i - 2], memo[i - 1])
    - These solved problems overlap, hence we can solve the full problem using
        our optimal substructure.
"""

def optimal_sale_profit(houses: list[int]) -> list:
    """
    Finds the max profit after selling to an optimal set of houses.
    
    Time complexity: O(n) where n is the no. of houses
    Space complexity: O(n) auxillary space
    """
    N = len(houses)
    if N == 0:
        return 0
    if N == 1:
        return houses[0]
    
    # Create memo array
    memo = [None] * N
    
    # Base cases
    memo[0] = houses[0]
    memo[1] = max(houses[0], houses[1])
    
    # Optimal substructure
    for i in range(2, N):
        memo[i] = max(houses[i] + memo[i - 2], memo[i - 1])
    
    return memo[N - 1]

def optimal_sale_houses(houses: list[int]) -> list:
    """
    Find the optimal set of houses after selling to them for max profit.
    
    Time complexity: O(n) where n is the no. of houses
    Space complexity: O(n) auxillary space
    """
    N = len(houses)
    if N == 0:
        return 0
    if N == 1:
        return houses[0]
    
    # Create memo array
    memo = [None] * N
    
    # Base cases
    memo[0] = houses[0]
    memo[1] = max(houses[0], houses[1])
    
    # Track decisions
    decisions = [False] * N
    decisions[0] = True
    decisions[1] = houses[1] > houses[0] # Did we sell house 1 or 0
    
    # Optimal substructure
    for i in range(2, N):
        sell_profit = houses[i] + memo[i - 2]
        skip_profit = memo[i - 1]
        
        if sell_profit >= skip_profit:
            memo[i] = sell_profit
            decisions[i] = True # We sell this house
        
        if sell_profit < skip_profit:
            memo[i] = skip_profit
            decisions[i] = False # We skip this house
        
    # Backtrack to find which houses were sold
    houses_sold = []
    i = N - 1
    while i >= 0:
        if decisions[i]:
            houses_sold.append(i)
            i -= 2 # Skip the adjacent house
        else:
            i -= 1 # Move to the previous house
            
    houses_sold.reverse()
    
    return houses_sold

if __name__ == '__main__':
    houses = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
    profit = optimal_sale_profit(houses)
    sold = optimal_sale_houses(houses)
    sold_values = [houses[i] for i in sold]
    assert profit == 252, f'Expected $252, got ${profit}'
    print(f'Maximum profit: ${profit}')
    print(f'Houses sold to (indices): {sold}')
    print(f'Values of houses sold to: {sold_values}')
    print("Passed")
