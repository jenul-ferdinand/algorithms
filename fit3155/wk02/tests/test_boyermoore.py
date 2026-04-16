from fit3155.wk02.src.boyermoore_basic import boyermoore_basic
from fit3155.wk02.src.boyermoore_extendedbcr import boyermoore_extendedbcr
from fit3155.wk02.src.boyermoore_gs import boyermoore_goodsuffix
from fit3155.wk02.src.boyermoore_mp import boyermoore_mp
from fit3155.wk02.src.boyermoore_optimised import boyermoore_optimised
from fit3155.wk02.src.models import BMOutput


def test_boyermoore_basic_bcr_one_match():
    pat = "thy"
    txt = "sphoorythy"
    matches = 1
    match_positions = [7]

    funcs = [boyermoore_basic, boyermoore_extendedbcr]
    for f in funcs:
        out = f(pat, txt)
        assert out.matches == matches
        assert out.match_positions == match_positions


def test_boyermoore_basic_bcr_no_match():
    pat = "abc"
    txt = "xyzsomething"
    matches = 0
    match_positions = []

    funcs = [boyermoore_basic, boyermoore_extendedbcr]
    for f in funcs:
        out = f(pat, txt)
        assert out.matches == matches
        assert out.match_positions == match_positions


def test_perfectly_fitting_match_at_end():
    """
    This will fail if while loop condition is k < n - m not k <= n - m
    """
    txt = "bbbacbacabbabcaabbbbbabcccbaccabcabc"
    pat = "abc"

    bm_gs: BMOutput = boyermoore_goodsuffix(pat, txt)
    bm_ebcr: BMOutput = boyermoore_extendedbcr(pat, txt)
    bm_basic: BMOutput = boyermoore_basic(pat, txt)

    assert bm_gs.match_positions == bm_ebcr.match_positions
    assert bm_gs.match_positions == bm_basic.match_positions
    assert bm_gs.match_positions == bm_basic.match_positions


def test_time_complexity():
    n = 1000
    m = n // 2
    txt = "a" * n
    pat = "a" * m

    opt: BMOutput = boyermoore_optimised(pat, txt)
    mp: BMOutput = boyermoore_mp(pat, txt)
    gs: BMOutput = boyermoore_goodsuffix(pat, txt)
    ebcr: BMOutput = boyermoore_extendedbcr(pat, txt)
    basic: BMOutput = boyermoore_basic(pat, txt)

    print("\n", "Character comparisons")
    print(opt.comparisons)
    print(mp.comparisons)
    print(gs.comparisons)
    print(ebcr.comparisons)
    print(basic.comparisons)

    assert opt.comparisons == n
    assert opt.comparisons < gs.comparisons
    assert (
        mp.comparisons
        == gs.comparisons
        == ebcr.comparisons
        == basic.comparisons
    )

    expected_quadratic_comparisons = m * (n - m + 1)

    assert mp.comparisons == expected_quadratic_comparisons
    assert gs.comparisons == expected_quadratic_comparisons
    assert ebcr.comparisons == expected_quadratic_comparisons
    assert basic.comparisons == expected_quadratic_comparisons
