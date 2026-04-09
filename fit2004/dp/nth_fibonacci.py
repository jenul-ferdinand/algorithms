import time
import sys

sys.setrecursionlimit(10_000)

def fib_basic(n: int) -> int:
    """
    Nth Fib Number (basic)
    
    Time Complexity: O(2^n)
    """
    if n == 0 or n == 1:
        return n
    
    return fib_basic(n - 1) + fib_basic(n - 2)

def fib_bottom_up(n):
    """
    Nth Fib Number (bottom up)
    
    Time Complexity: O(n)
    """
    memo = [None] * (n+1)
    memo[0] = 0
    memo[1] = 1
    
    for i in range(2, n+1): 
        memo[i] = memo[i-1] + memo[i-2]
    
    return memo[n]

def fib_top_down(n):
    """
    Nth Fib Number (top down)
    
    Time Complexity: O(n)
    """
    memo = [None] * (n+1)
    memo[0] = 0
    memo[1] = 1
    
    def fib(n):
        if memo[n] is not None:
            return memo[n]

        memo[n] = fib(n-1) + fib(n-2)
        return memo[n]
    
    return fib(n)
    


if __name__ == '__main__':
    res = fib_basic(10)
    print(res)

    res = fib_bottom_up(10)
    print(res)
    
    res = fib_top_down(10)
    print(res)

