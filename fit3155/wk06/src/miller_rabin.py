import random

from fit3155.wk06.src.modexp import modexp


def miller_rabin(n: int, k: int = 10):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    # Find s and t such that n - 1 = 2^s * t, with t being odd
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(k):
        # A random witness
        a = random.randint(2, n - 2)

        # Building the sequence
        # x[0], x[1], ..., x[s] by repeated squaring
        x = [None] * (s + 1)
        x[0] = modexp(a, t, n)  # x[0] = a^t mod n;
        for i in range(1, s + 1):
            x[i] = modexp(x[i - 1], 2, n)  # x[i] = x[i-1]^2 mod n

        # Fermat check
        # x[s] = a^(n-1) mod n must be 1
        if x[s] != 1:
            return False

        # Miller-Rabin's check
        # any x[i] = 1 must come from x[i-1] = 1 or x[i-1] = n-1
        for i in range(1, s + 1):
            if x[i] == 1 and x[i - 1] != 1 and x[i - 1] != n - 1:
                return False

    return True


if __name__ == "__main__":
    is_prime = miller_rabin(561)
    print(is_prime)
