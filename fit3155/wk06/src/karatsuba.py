"""
Recurrence: T(2d) = 3T(d) + cd
"""


def karatsuba(u: int, v: int):
    """
    Divide and conquer multiplication

    Time complexity: O(n^log(3)) = O(n^1.585)
    Space complexity: O(n) in bit length
    """
    # Base case: one bit multiplication
    if u <= 1 or v <= 1:
        return u * v
    
    n = max(u.bit_length(), v.bit_length())
    d = n // 2

    # Halfing
    # U1,V1 store the most significant bits half 
    # U0,V0 store the least significant bits half
    U1 = u >> d
    U0 = u & ((1 << d) - 1)
    V1 = v >> d 
    V0 = v & ((1 << d) - 1)

    A = karatsuba(U1, V1)
    B = karatsuba(U0, V0)
    C = karatsuba(U1 - U0, V1 - V0)

    # Karatsuba's optimisation
    # this ensures that we save one multiplication
    # because (U1-U0)(V1-V0) = U1V1 - U1V0 - U0V1 + U0V0
    # U1V0 and U0V1 is what we need, no need for two multiplications.
    middle = A + B - C 

    # Karatsuba formula: 2^2d A + 2^d middle + B
    return (A << (2 * d)) + (middle << d) + B


if __name__ == "__main__":
    u = 12
    v = 10
    res = karatsuba(u, v)
    assert res == 120
