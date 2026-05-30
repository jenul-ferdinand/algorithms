def modexp(a: int, b: int, n: int):
    """
    Modular exponentiation with repeated squaring

    Definitions:
    - x is the current bit we're looking at when looping through b[LSB..MSB]
    - c is the current squared power of the base
    - r is the running result

    Rules per iteration:
    (1) c = (c * c) mod n
    (2) r = (r * c) mod n, iff x == 1
    """
    b = bin(b)[2:]

    # Base case
    c = a % n

    if b[-1] == "1":
        r = c
    else:
        r = 1
    
    # Remaining bits LSB -> MSB
    for x in reversed(b[:-1]):
        c = (c * c) % n # rule 1
        if x == "1":
            r = (r * c) % n # rule 2

    return r
