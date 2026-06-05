from fit3155.wk06.src.miller_rabin import miller_rabin

if __name__ == "__main__":
    for n in range(10_000):
        is_prime = miller_rabin(n)
        if is_prime:
            print(n)
