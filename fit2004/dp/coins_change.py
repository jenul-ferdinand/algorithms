import math

INFINITY = math.inf

def coins_change_top_down(coins: list, target: int):
    """
    Finds the minimum number of coins needed that add up to the target value
    given a set of coins.
    
    Recurrence:
        1. mc[0] = 0
        2. mc[T] = INFINITY if T > 0 and v < C[i] for all i
        Otherwise,
        3. mc[T] = min(1 + mc[T - C[i]]) 
    """
    memo = [-1] * (target+1)
    
    def solve(coins: list, target: int):
        # Reccurence case 1
        if target == 0: return 0
        
        if memo[target] == -1:
            # Recurrence case 2
            min_coins = INFINITY
            
            for i in range(len(coins)):
                if coins[i] <= target:
                    # Recurrence step 3
                    min_coins = min(
                        min_coins,  
                        1 + solve(coins, target - coins[i])
                    )
            
            memo[target] = min_coins
        
        return memo[target]
    
    return solve(coins, target)

def coins_change_bottom_up(coins: list[int], target: int) -> float:
    """
    Bottom-up DP for the coin-change problem.
    
    Builds a table memo[0..target] where
    dp[t] = minimum coins needed to make sum t,
    or INFINITY if t cannot be formed.
    
    Time Complexity: O(target * len(coins))
    Space Complexity: O(target)
    """
    memo = [INFINITY] * (target + 1)
    memo[0] = 0
    
    for t in range(1, target + 1):
        best = INFINITY
        for c in coins:
            if c <= t:
                best = min(best, memo[t-c]+1)
        memo[t] = best
        
    return memo[target]

if __name__ == '__main__':
    # Test 1
    coins = [1]
    target = 3
    res1 = coins_change_top_down(coins, target)
    res2 = coins_change_bottom_up(coins, target)
    exp = 3
    assert res1 == exp, f'Expected {exp}, got {res1}'
    assert res1 == res2, f'Bottom up version failed' 
    
    # Test 2
    coins = [2,3,9]
    target = 12
    res1 = coins_change_top_down(coins, target)
    res2 = coins_change_bottom_up(coins, target)
    exp = 2
    assert res1 == exp, f'Expected {exp}, got {res1}'
    assert res1 == res2, f'Bottom up version failed'
    
    print('All tests passed!')