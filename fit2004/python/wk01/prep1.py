def fib_recursive(n):
    '''
    Space Complexity: O(n)
    Time Complexity: O(2^n)
    '''
    if n == 0: 
        return 0
    if n == 1:
        return 1
    
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_iterative(n):
    '''
    Space Complexity: O(1)
    Time Complexity: O(n) 
    '''
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a = 0
    b = 1
    
    for _ in range(2, n + 1):
        temp = a + b
        a = b
        b = temp
        
    return b

def karatsuba(x,y):
    # We get the length of digits of both x and y
    n = len(str(x)) + len(str(y))
    
    # Base cases
    if n==1 or n==2 or n==3:
        return x * y
    
    # Get the length in digits of half of both x and y
    x_half_length = int(len(str(x))/2)
    y_half_length = int(len(str(y))/2)
    
    # Split in half both x and y
    x_left, x_right = int(str(x)[:x_half_length]), int(str(x)[x_half_length:])
    y_left, y_right = int(str(y)[:y_half_length]), int(str(x)[y_half_length:])
    
    u = x_left + x_right
    v = y_left + y_right
    
    a = karatsuba(x_left, x_right)
    b = karatsuba(y_left, y_right)
    c = karatsuba(u, v)
    
    z = c - a - b
    return a * 10**n + z * 10**(n/2) + b

if __name__ == '__main__':
    #print(fib_recursive(5))
    #print(fib_iterative(5))
    print(karatsuba(323, 32312))      