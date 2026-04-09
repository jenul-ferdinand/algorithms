def zalg(string: str) -> list[int]:
    """
    Z-Algorithm

    Let n be the size of the input string.

    Time complexity: O(n)
        We take n iterations to complete the z array.
    Space complexity: O(n)
        We create a z array of size n.

    """
    n = len(string)  # 18
    z = [0] * n
    z[0] = n
    print("set 0th index to n")

    left, right = -1, -1

    for k in range(1, n):
        k_mirror = k - left
        zbox_offset = right - k

        # case 1 (k > r)
        if k > right:
            print("case 1")
            i = 0
            while k + i < n and string[i] == string[k + i]:
                i += 1
            z[k] = i
            if z[k] > 0:
                left = k
                right = k + z[k]
        # case 2 (k <= r)
        elif k <= right:
            z[k] = min(z[k_mirror], right - k)

            if z[k_mirror] == zbox_offset:
                i = 0
                while (
                    right + i < n and string[right + i] == string[right - k + i]
                ):
                    i += 1
                z[k] += i
                if z[k] > 0:
                    left = k
                    right = k + z[k]

            # # 2a: fully contained within zbox
            # if z[k_mirror] < zbox_offset:
            #     print('case 2a: reused previous value')
            #     z[k] = z[k_mirror]

            # # 2b
            # elif z[k_mirror] >= zbox_offset:
            #     print('case 2b + possibly 2c')
            #     z[k] = right - k
            #     # 2c: extend past right of zbox
            #     if z[k_mirror] == zbox_offset:
            #         i = 0
            #         while right + i < n and string[right + i] == string[right - k + i]:
            #             i += 1
            #         z[k] += i
            #         if z[k] > 0:
            #             left = k
            #             right = k + z[k]

    return z


if __name__ == "__main__":
    z = zalg("aabcaabxaabcaabcay")
    print(z)

    correct = [18, 1, 0, 0, 3, 1, 0, 0, 7, 1, 0, 0, 5, 1, 0, 0, 1, 0]
    assert z[0] == correct[0]
    assert z == correct, f"\nExpected {correct},\nGot      {z}"

    del z
    del correct
    print("\n")

    z = zalg("abaaba")
    print(z)

    correct = [6, 0, 1, 3, 0, 1]
    assert z == correct, f"\nExpected {correct},\nGot      {z}"

    del z
    del correct
    print("\n")

    z = zalg("aaaaaaaa")
    print(z)
