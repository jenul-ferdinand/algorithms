def zalg(string: str) -> list[int]:
    """
    Z-Algorithm

    Let n be the size of the input string.

    Time complexity: O(n)
        We take n iterations to complete the z array.
    Space complexity: O(n)
        We create a z array of size n.

    """
    n = len(string)
    if n <= 0:
        return []

    z = [0] * n
    z[0] = n

    left, right = -1, -1

    for k in range(1, n):
        # Case 1
        if k > right:
            i = 0
            while k + i < n and string[i] == string[k + i]:
                i += 1
            z[k] = i
            if z[k] > 0:
                left = k
                right = k + z[k]
        # Case 2
        elif k <= right:
            z[k] = min(z[k - left], right - k)

            if z[k - left] == right - k:
                i = 0
                while (
                    right + i < n and string[right + i] == string[right - k + i]
                ):
                    i += 1
                z[k] += i
                if z[k] > 0:
                    left = k
                    right = k + z[k]

    return z
