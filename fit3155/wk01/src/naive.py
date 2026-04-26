from fit3155.wk01.src.models import ZalgOutput


def naive(string: str) -> ZalgOutput:
    output = ZalgOutput()

    n = len(string)
    if n <= 0:
        return output
    z = [0] * n
    z[0] = n

    for k in range(1, n):
        output.case1_times += 1

        i = 0
        while k + i < n:
            output.comparisons += 1
            if string[i] != string[k + i]:
                break
            i += 1

        z[k] = i

    output.z_array = z

    output.zbox_updates = None
    output.case2_times = None
    output.reuse_times = None
    output.clamp_times = None
    output.extensions = None

    return output


# if __name__ == "__main__":
#     z = naive("abxbab")
#     print(z)
#     assert z == [6, 0, 0, 0, 2, 0]
