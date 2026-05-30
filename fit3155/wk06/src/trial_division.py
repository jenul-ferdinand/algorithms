def trial_division(n: int):
    """
    Naive primarily test using trial division
    """
    for k in range(2, n):
        if k % n == 0:
            # n | k so prime
            return True
    # no factor was found, so not prime
    return False
