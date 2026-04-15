from fit3155.wk02.src.boyermoore_mp import boyermoore_mp, process_mp
from fit3155.wk02.src.models import BMOutput


def test_mp_array_from_notes():
    pat = "acababacaba"
    mp = process_mp(pat)
    assert mp == [11, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 0]


def test_matched_prefix():
    txt = "axcabcab"
    pat = "abcab"

    bm_gs: BMOutput = boyermoore_mp(pat, txt)

    print(bm_gs)

    assert bm_gs.matches == 1
    assert bm_gs.match_positions == [3]
