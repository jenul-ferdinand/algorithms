from fit3155.wk02.src.boyermoore_basic import boyermoore_basic
from fit3155.wk02.src.boyermoore_extendedbcr import boyermoore_extendedbcr
from fit3155.wk02.src.models import BMOutput


def test_bcr_vs_extended_bcr():
    text = "a" * 10_000 + "cbcbcb" + "c" * 100 + "cbc" + "ccccccbcbc"
    pattern = "cbc"

    bcr: BMOutput = boyermoore_basic(pat=pattern, txt=text)
    ebcr: BMOutput = boyermoore_extendedbcr(pat=pattern, txt=text)

    print(bcr.compares)
    print(ebcr.compares)

    print(bcr.shifts)
    print(ebcr.shifts)

    assert True


def test_extended_bcr_does_equal_or_less_comparisons_vs_basic_bcr():
    cases = [
        ("a" * 10_000 + "cbcbcb", "cbc"),
        ("b" * 10_000, "xyab"),
        ("b" * 10_000, "xxxxxxxxab"),
        ("abracadabra" * 1000, "cad"),
    ]
    for text, pat in cases:
        basic = boyermoore_basic(pat, text)
        ext = boyermoore_extendedbcr(pat, text)
    assert ext.match_positions == basic.match_positions, (
        f"disagreement on correctness: {pat!r} in {text[:30]!r}..."
    )
    assert ext.compares <= basic.compares, (
        f"extended did MORE work than basic on pat={pat!r}: "
        f"basic={basic.compares}, ext={ext.compares}"
    )


def test_extended_bcr_strictly_beats_basic_bcr():
    text = "b" * 10_000
    pattern = "xxxxxxxxab"
    basic = boyermoore_basic(pattern, text)
    ext = boyermoore_extendedbcr(pattern, text)
    # basic shifts by 1 each time, extended by 9 
    # --> expect 3x fewer comparisons
    ratio = basic.compares / ext.compares
    assert ratio > 3, (
        f"expected 3x speedup for Extended BCR, got {ratio:.1f}×"
    )
