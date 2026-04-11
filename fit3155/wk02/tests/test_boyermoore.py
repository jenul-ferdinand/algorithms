from fit3155.wk02.src.boyermoore_basic import boyermoore_basic
from fit3155.wk02.src.boyermoore_extendedbcr import boyermoore_extendedbcr


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
