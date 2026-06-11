from fit3155.wk01.src.models import ZalgOutput


def zalg(S: str) -> ZalgOutput:
    """
    Z-Algorithm

    Let n be the size of the input string.

    Time complexity: O(n)
        We take n iterations to complete the z array.
    Space complexity: O(n)
        We create a z array of size n.

    """
    _metadata = ZalgOutput()

    n = len(S)
    if n <= 0:
        return _metadata

    Z = [0] * n
    Z[0] = n

    left, right = -1, -1

    for k in range(1, n):
        # Case 1: Naive comparisons
        # when we have no information past the sliding window
        if k > right:
            _metadata.case1_times += 1

            i = 0
            while k + i < n:
                _metadata.comparisons += 1

                if S[i] != S[k + i]:
                    break  # mismatch
                i += 1
            Z[k] = i
            if Z[k] > 0:
                _metadata.zbox_updates += 1

                left = k
                right = k + Z[k] - 1

        # Case 2: Optimisations using sliding window
        elif k <= right:
            _metadata.case2_times += 1

            prefix_right = right - k + 1
            prefix_k = k - left
            zbox_right = right + 1

            # Reusing previous value (2a)
            if Z[prefix_k] < prefix_right:
                _metadata.reuse_times += 1

                Z[k] = Z[prefix_k]

            # Clamping with remaining distance from k -> R (2b)
            elif Z[prefix_k] > prefix_right:
                _metadata.clamp_times += 1

                Z[k] = prefix_right

            # Extending from R naively (2c)
            elif Z[prefix_k] == prefix_right:
                i = 0
                while zbox_right + i < n:
                    # naive comparison past right of zbox
                    _metadata.comparisons += 1

                    if S[zbox_right + i] != S[prefix_right + i]:
                        break
                    i += 1

                if i > 0:
                    _metadata.extensions += 1

                Z[k] = prefix_right + i
                if Z[k] > 0:
                    _metadata.zbox_updates += 1

                    left = k
                    right = k + Z[k] - 1

    _metadata.z_array = Z

    return _metadata
