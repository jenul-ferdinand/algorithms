from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk02.src.boyermoore_extendedbcr import boyermoore_extendedbcr
from fit3155.wk02.src.boyermoore_gs import (
    boyermoore_goodsuffix,
    process_gs,
    process_z_suffix,
)
from fit3155.wk02.src.models import BMOutput


def test_z_suffix_array_from_notes():
    z_suffix = process_z_suffix("acababacaba")
    assert z_suffix == [1, 0, 1, 0, 5, 0, 3, 0, 1, 0, 0, 0]


def test_gs_array_from_notes():
    pat = "acababacaba"
    z_suffix = process_z_suffix(pat)
    gs_array = process_gs(pat, z_suffix)
    assert gs_array == [0, 0, 0, 0, 0, 0, 4, 0, 6, 0, 8, 10]


def test_basic():
    txt = "acxccyxbabacabaa"
    pat = "acababacaba"
    out: BMOutput = boyermoore_goodsuffix(pat, txt)

    # The pattern shifts twice using good suffix rule in this example.
    #
    # txt: acxccyxbabacabaa
    # pat: acababacaba
    #             ^ mismatch here at j=7, gs[8]=6=p, shift=m-p-1=11-6-1=4
    #
    # txt: acxccyxbabacabaa
    # pat:     acababacaba              (shifted pattern 4 places)
    #            ^ mismatch here at j=2, gs[3]=0=p, shift=11-0-1=10
    #
    # txt: acxccyxbabacabaa
    # pat:               acababacaba    (shifted pattern 10 places)
    #
    # Exit while. No more possibilites.

    assert out.gs_shifts == 2

    # Never in any iteration was gs_shift < bcr_shift.
    assert out.bcr_shifts == 0

    assert out.matches == 0
    assert out.matched_comparisons == 11


@given(st.text(alphabet="abc", min_size=500, max_size=2500))
def test_goodsuffix_vs_extended_bcr(txt):

    pat = "abc"

    bm_gs: BMOutput = boyermoore_goodsuffix(pat, txt)
    bm_ebcr: BMOutput = boyermoore_extendedbcr(pat, txt)

    # In general, goodsuffix rule gives fewer comparisons in total
    assert bm_gs.comparisons <= bm_ebcr.comparisons

    assert bm_gs.match_positions == bm_ebcr.match_positions
