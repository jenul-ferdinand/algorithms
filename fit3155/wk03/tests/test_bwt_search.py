from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk03.src.bwt_search import bwt_search


def naive_search(pat: str, txt: str) -> list[int]:
    m = len(pat)
    return [
        i for i in range(len(txt) - m + 1) if txt[i : i + m] == pat
    ]


def test_bwt_search_single_match():
    txt = "banana"
    pat = "nan"

    assert sorted(bwt_search(pat, txt)) == [2]


def test_bwt_search_multiple_matches():
    txt = "banana"
    pat = "ana"

    assert sorted(bwt_search(pat, txt)) == [1, 3]


def test_bwt_search_no_match():
    txt = "banana"
    pat = "apple"

    assert bwt_search(pat, txt) == []


def test_bwt_search_whole_text():
    txt = "banana"
    pat = "banana"

    assert sorted(bwt_search(pat, txt)) == [0]


def test_bwt_search_single_character():
    txt = "banana"
    pat = "a"

    assert sorted(bwt_search(pat, txt)) == [1, 3, 5]


def test_bwt_search_boundaries():
    txt = "abcxabcd"

    assert sorted(bwt_search("abc", txt)) == [0, 4]
    assert sorted(bwt_search("cd", txt)) == [6]


def test_bwt_search_against_naive_examples():
    txt = "abracadabra"

    for pat in ["a", "ab", "bra", "ra", "cad", "xyz"]:
        assert sorted(bwt_search(pat, txt)) == naive_search(pat, txt)


@given(
    txt=st.text(alphabet="abc", min_size=1, max_size=25),
    pat=st.text(alphabet="abc", min_size=1, max_size=8),
)
def test_bwt_search_against_naive_hypothesis(txt: str, pat: str):
    if len(pat) > len(txt):
        return

    assert sorted(bwt_search(pat, txt)) == naive_search(pat, txt)
