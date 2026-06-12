from fit3155.wk02.src.boyermoore_gs import process_gs, process_z_suffix
from fit3155.wk02.src.boyermoore_mp import process_mp
from fit3155.wk02.src.models import BMOutput


def boyermoore_optimised(pat: str, txt: str) -> BMOutput:
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

    # Precompute the matched prefix array
    mp = process_mp(pat)

    output.mp = mp

    start = 0
    stop = -1

    j = 0
    while j <= n - m:
        gs_shift = 0
        gs_shift_source = None

        # Right to left scanning
        k = m - 1
        while k >= 0:
            # Galil's optimisation: skipping known segment
            if k == stop:
                k = start - 1
                output.galil_skips += 1
                if k < 0:
                    break

            output.comparisons += 1

            if pat[k] != txt[j + k]:
                if k < m - 1:
                    # Good suffix rule
                    p = gs[k + 1]

                    if p > 0:
                        gs_shift = m - 1 - p
                        gs_shift_source = "gs"

                        start = p - m + k + 2
                        stop = p - 1

                    # Matched prefix rule
                    elif p == 0:
                        gs_shift = m - mp[k + 1]
                        gs_shift_source = "mp"

                        start = 0
                        stop = mp[k + 1] - 1
                break

            output.matched_comparisons += 1
            k -= 1

        j_before = j
        if k == -1:
            # Full match
            output.matches += 1
            output.match_positions.append(j)

            output.mp_shifts += 1
            shift = m - mp[1]

            start = 0
            stop = mp[1] - 1
        else:
            # Extended bad character rule
            x = txt[j + k]
            badchar_shift = k - R[k][ord(x)]

            # Shifting either with good suffix or ext bad char shift
            if gs_shift > badchar_shift:
                shift = gs_shift

                if gs_shift_source == "mp":
                    output.mp_shifts += 1
                elif gs_shift_source == "gs":
                    output.gs_shifts += 1
            else:
                output.bcr_shifts += 1
                shift = badchar_shift

                start = 0
                stop = -1

        j += shift

        assert j > j_before, "Must shift forwards at least one position"
        output.total_shifts += 1

    return output
