from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk04.src.NaiveSuffixTree import NaiveSuffixTree
from fit3155.wk04.src.Ukkonen01Naive import UkkonenNaive
from fit3155.wk04.src.Ukkonen02SuffixLinks import (
    UkkonenSuffixLinks,
)
from fit3155.wk04.src.Ukkonen03SkipCount import UkkonenSkipCount
from fit3155.wk04.tests._serialize import _serialize

# Tree correctness
@given(st.text(alphabet="abc", max_size=100))
def test_tree_structure_matches_upto_03(S):
    S = S + "$"
    stnaive = NaiveSuffixTree(S)
    uknaive = UkkonenNaive(S)
    uksuff = UkkonenSuffixLinks(S)
    ukskipcount = UkkonenSkipCount(S)
    assert (
        _serialize(uknaive.r, S)
        == _serialize(uksuff.r, S)
        == _serialize(stnaive.r, S)
        == _serialize(ukskipcount.r, S)
    )
