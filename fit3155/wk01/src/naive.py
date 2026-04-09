def naive(string: str) -> list[int]:
    n = len(string)  # 6
    z = [0] * n
    z[0] = n

    for k in range(1, n):
        i = 0
        while k + i < n and string[i] == string[k + i]:
            i += 1
        z[k] = i

    return z


if __name__ == "__main__":
    z = naive("abxbab")
    print(z)
    assert z == [6, 0, 0, 0, 2, 0]
