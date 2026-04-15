from fit3155.wk02.src.boyermoore_mp import boyermoore_mp
from fit3155.wk02.src.boyermoore_optimised import boyermoore_optimised


def test_galils():
    txt = "a" * 10
    pat = "aa"

    bm_opt = boyermoore_optimised(pat, txt)
    bm_mp = boyermoore_mp(pat, txt)

    # Correctness
    assert bm_opt.match_positions == bm_mp.match_positions == list(range(9))
    assert bm_opt.matches == 9

    # Exact comparison count and skip count from galil's
    assert bm_opt.comparisons == 10
    assert bm_opt.galil_skips == 8

    # Optimisation drastically reduces comparisons
    assert bm_opt.comparisons < bm_mp.comparisons


def test_galils_beats_mp_on_notes_worst_case():
    txt = "a" * 20
    pat = "aaa"

    bm_opt = boyermoore_optimised(pat, txt)
    bm_mp = boyermoore_mp(pat, txt)

    assert bm_opt.match_positions == bm_mp.match_positions

    # Without Galil: m comparisons per alignment
    # -> roughly m * (n - m + 1) = 3 * 18 = 54.
    #
    # With Galil: m for the first alignment, then 1 per subsequent 
    # -> 3 + 17 = 20.
    assert bm_mp.comparisons == 54
    assert bm_opt.comparisons == 20
