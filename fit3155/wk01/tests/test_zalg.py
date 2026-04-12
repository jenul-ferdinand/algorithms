from hypothesis import assume, given
from hypothesis import strategies as st

from fit3155.wk01.src.models import ZalgOutput
from fit3155.wk01.src.naive import naive
from fit3155.wk01.src.zalg import zalg


@given(st.text(alphabet="ab", max_size=50))
def test_zalg_vs_naive(txt):
    zalg_out: ZalgOutput = zalg(txt)
    naive_out: ZalgOutput = naive(txt)
    assert zalg_out.z_array == naive_out.z_array
    assert zalg_out.comparisons <= naive_out.comparisons


@given(st.text(alphabet="ab", max_size=30))
def test_naive_invariants(txt):
    out: ZalgOutput = naive(txt)
    n = len(txt)

    assume(n > 1)

    assert out.case1_times == n - 1
    assert out.case2_times is None


@given(st.text(alphabet="ab", max_size=100))
def test_zalg_invariants(txt):
    out: ZalgOutput = zalg(txt)
    n = len(txt)

    assume(n > 10)

    # Every position k=1...n-1 is exactly one of Case 1 or Case 2
    assert out.case1_times + out.case2_times == n - 1

    # Every case 2 is either a reuse (2a) or a clamp (2b)
    assert out.reuse_times + out.clamp_times == out.case2_times

    # The algorithm is O(n), comparisons should not be more than 2n
    assert out.comparisons < 2 * n


funcs = [naive, zalg]


def test_repeating():
    for f in funcs:
        out: ZalgOutput = f("aaaaaaa")
        assert out.z_array == [7, 6, 5, 4, 3, 2, 1]


def test_no_matches():
    for f in funcs:
        out: ZalgOutput = f("abcde")
        assert out.z_array == [5, 0, 0, 0, 0]


def test_empty_string():
    for f in funcs:
        out: ZalgOutput = f("")
        assert out.z_array == []


def test_single_character():
    for f in funcs:
        out: ZalgOutput = f("a")
        assert out.z_array == [1]


def test_examples_from_notes():
    for f in funcs:
        out: ZalgOutput = f("aabcaabxaabcaabcay")
        assert out.z_array == [
            18,
            1,
            0,
            0,
            3,
            1,
            0,
            0,
            7,
            1,
            0,
            0,
            5,
            1,
            0,
            0,
            1,
            0,
        ]
