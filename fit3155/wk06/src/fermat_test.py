import random

from fit3155.wk06.src.modexp import modexp


def fermat_test(n: int, k: int = 10) -> bool:
    """
    Randomised primality testing using fermat's little therom

    Returns boolean:
    - False: definitely composite.
    - True: probably prime, unless n was a Carmichael number.
    """
    if n < 2:
        return False  # 0 and 1 are not prime
    if n < 4:
        return True  # 2 and 3 are prime

    for _ in range(k):
        a = random.randint(2, n - 2)
        if modexp(a, n - 1, n) != 1:
            return False  # witness found, definitely composite

    return True  # passed all k rounds, probably prime.


if __name__ == "__main__":
    is_prime = fermat_test(13331)
    print(is_prime)
