def fib1(n):
    '''
    Calculates the n-th fibonacci number
    
    Time Complexity: O(2^n)
    Space Complexity: O(n)
    
    Recurrence Relation:
        F(0) = 0
        F(1) = 1
        F(k) = F(n-1)+F(n-2)
    '''
    if n == 0: return 0
    if n == 1: return 1
    
    return fib1(n-1) + fib1(n-2)

def fib2(n):
    '''
    Calculates the n-th fibonacci number
    
    Time Complexity: 
    Space Complexity: O(n)
    
    Recurrence Relation:
        F(0) = 0
        F(1) = 1
        F(2k) = F(k)[2F(k+1)-F(k)]
        F(2k+1) = F(k+1)^2 + F(k)^2
    '''
    if n == 0: return 0
    if n == 1: return 1
    
    if n % 2 == 0:
        return fib2(n) * ((2*fib2(n+1))-fib2(n))
    else:
        return fib2(n+1)**2 + fib2(n)**2
    
if __name__ == '__main__':
    print(fib1(10))
    
    assert fib1(0) == 0
    assert fib1(1) == 1
    assert fib1(10) == 55
    
    assert fib2(0) == 0
    assert fib2(1) == 1
    
    # print(fib2(10))