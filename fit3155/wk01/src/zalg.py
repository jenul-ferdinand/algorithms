from fit3155.wk01.src.models import ZalgOutput


def zalg(string: str) -> ZalgOutput:
    """
    Z-Algorithm

    Let n be the size of the input string.

    Time complexity: O(n)
        We take n iterations to complete the z array.
    Space complexity: O(n)
        We create a z array of size n.

    """
    output = ZalgOutput()

    n = len(string)
    if n <= 0:
        return output

    z = [0] * n
    z[0] = n

    left, right = -1, -1

    for k in range(1, n):
        # Case 1: Naive comparisons
        # When we have no information past the sliding window
        if k > right:
            output.case1_times += 1

            i = 0
            while k + i < n:
                output.comparisons += 1
                if string[i] != string[k + i]:
                    break # mismatch
                i += 1
            z[k] = i
            if z[k] > 0:
                output.zbox_updates += 1
                left = k
                right = k + z[k]

        # Case 2: Optimisations using sliding window
        elif k <= right:
            output.case2_times += 1

            # Reusing previous value (2a)
            if z[k - left] < right - k:
                output.reuse_times += 1
                z[k] = z[k - left]

            # Clamping with remaining distance from k -> R (2b)
            elif z[k - left] >= right - k:
                output.clamp_times += 1
                z[k] = right - k

            # Extending from R naively (2c)
            if z[k - left] == right - k:
                i = 0
                while right + i < n:
                    output.comparisons += 1
                    if string[right + i] != string[right - k + i]:
                        break # mismatch
                    i += 1

                if i > 0:
                    output.extensions += 1

                z[k] += i
                if z[k] > 0:
                    output.zbox_updates += 1
                    left = k
                    right = k + z[k]

    output.z_array = z

    return output
