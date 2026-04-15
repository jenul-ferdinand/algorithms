from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk02.src.boyermoore_basic import boyermoore_basic
from fit3155.wk02.src.boyermoore_extendedbcr import boyermoore_extendedbcr
from fit3155.wk02.src.models import BMOutput


@given(st.text(alphabet="abc", min_size=900, max_size=1500))
def test_bcr_vs_extended_bcr(txt):
    pattern = "bbc"

    bcr: BMOutput = boyermoore_basic(pat=pattern, txt=txt)
    ebcr: BMOutput = boyermoore_extendedbcr(pat=pattern, txt=txt)

    # Extended BCR will generally have less comparisons than BCR
    # because we optimised to shift more
    assert ebcr.comparisons <= bcr.comparisons

    # Extended BCR should have less shifts, because it shifts more efficiently.
    assert ebcr.total_shifts <= bcr.total_shifts

    # Compared correctness
    assert bcr.match_positions == ebcr.match_positions
    assert bcr.matches == ebcr.matches


def test_extended_bcr_does_equal_or_less_comparisons_vs_basic_bcr():
    cases = [
        ("a" * 10_000 + "cbcbcb", "cbc"),
        ("b" * 10_000, "xyab"),
        ("b" * 10_000, "xxxxxxxxab"),
        ("abracadabra" * 1000, "cad"),
    ]

    for text, pat in cases:
        basic: BMOutput = boyermoore_basic(pat, text)
        ext: BMOutput = boyermoore_extendedbcr(pat, text)
    assert ext.match_positions == basic.match_positions, (
        f"disagreement on correctness: {pat!r} in {text[:30]!r}..."
    )
    assert ext.comparisons <= basic.comparisons, (
        f"extended did MORE work than basic on pat={pat!r}: "
        f"basic={basic.comparisons}, ext={ext.comparisons}"
    )


def test_extended_bcr_strictly_beats_basic_bcr():
    text = "b" * 10_000
    pattern = "xxxxxxxxab"
    basic: BMOutput = boyermoore_basic(pattern, text)
    ext: BMOutput = boyermoore_extendedbcr(pattern, text)
    # basic shifts by 1 each time, extended by 9
    # --> expect 3x fewer comparisons
    ratio = basic.comparisons / ext.comparisons
    assert ratio > 3, f"expected 3x speedup for Extended BCR, got {ratio:.1f}×"
