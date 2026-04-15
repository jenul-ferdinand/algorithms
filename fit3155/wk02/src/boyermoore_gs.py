from fit3155.wk01.src.zalg import zalg
from fit3155.wk02.src.models import BMOutput


def process_z_suffix(pat: str) -> list[int]:
    pat_reverse = pat[::-1]
    z = zalg(pat_reverse).z_array

    z_suffix = z[::-1]

    z_suffix[-1] = 0  # useless last value
    z_suffix.append(0)  # add one more to match size of gs array

    return z_suffix


def process_gs(pat: str, z_suffix: list[int]) -> list[int]:
    n = len(z_suffix)
    m = len(pat)
    gs_array = [0] * n

    for p in range(m):
        j = m - z_suffix[p]
        gs_array[j] = p

    return gs_array


def boyermoore_goodsuffix(pat: str, txt: str) -> BMOutput:
    output = BMOutput()

    n = len(txt)
    m = len(pat)

    # Precompute the extended bad character shift table
    R = [[-1 for i in range(128)] for _ in range(m)]
    for i in range(1, m):
        R[i] = R[i - 1].copy()
        R[i][ord(pat[i - 1])] = i - 1

    # Precompute the good suffix array
    z_suffix = process_z_suffix(pat)
    gs = process_gs(pat, z_suffix)

    output.z_suffix = z_suffix
    output.goodsuffix = gs

    k = 0
    while k <= n - m:
        gs_shift = 0

        # Right to left scanning
        j = m - 1
        while j >= 0:
            output.comparisons += 1
            if pat[j] != txt[k + j]:
                if j < m - 1:
                    # Good suffix rule
                    p = gs[j + 1]
                    gs_shift = m - 1 - p
                break

            output.matched_comparisons += 1
            j -= 1

        k_before = k
        if j == -1:
            # Full match
            output.matches += 1
            output.match_positions.append(k)
            k += 1
        else:
            # Extended bad character rule
            x = txt[k + j]
            badchar_shift = j - R[j][ord(x)]

            # Shifting either with good suffix or ext bad char shift
            if gs_shift > badchar_shift:
                output.gs_shifts += 1
                shift = gs_shift
            else:
                output.bcr_shifts += 1
                shift = badchar_shift

            k += shift

        assert k > k_before, "Must shift forwards at least one position"
        output.total_shifts += 1

    return output
