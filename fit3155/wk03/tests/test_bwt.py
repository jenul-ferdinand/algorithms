from fit3155.common.constants import ASCII_LOWER
from fit3155.wk03.src.bwt import (
    bwt,
    process_LF,
    process_occ,
    process_rank,
)


def test_simple():
    string = "googol%"

    b = bwt(string)
    b_naive = bwt(string)

    answer = "lo%oogg"

    assert b == answer
    assert b_naive == answer


def test_rank_with_seminar_example():
    """
    L = lo%oogg -> F = %gglooo
        0123456        0123456
    """
    L = "lo%oogg"
    rank = process_rank(L)

    assert rank[ord("%") - ASCII_LOWER] == 0
    assert rank[ord("g") - ASCII_LOWER] == 1
    assert rank[ord("l") - ASCII_LOWER] == 3
    assert rank[ord("o") - ASCII_LOWER] == 4


def test_occ_with_seminar_example():
    L = "lo%oogg"
    occ = process_occ(L)

    assert occ[ord("%") - ASCII_LOWER] == [0, 0, 0, 1, 1, 1, 1, 1]
    assert occ[ord("g") - ASCII_LOWER] == [0, 0, 0, 0, 0, 0, 1, 2]
    assert occ[ord("l") - ASCII_LOWER] == [0, 1, 1, 1, 1, 1, 1, 1]
    assert occ[ord("o") - ASCII_LOWER] == [0, 0, 1, 1, 2, 3, 3, 3]


def test_lf_mapping():
    L = "lo%oogg"
    rank = process_rank(L)
    occ = process_occ(L)
    lf = process_LF(L, rank, occ)

    assert lf == [3, 4, 0, 5, 6, 1, 2]
