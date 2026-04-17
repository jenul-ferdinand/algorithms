from fit3155.wk03.src.suffix_array_naive import suffix_array_naive
from fit3155.wk03.src.suffix_array_prefix_doubling import (
    suffix_array_prefix_doubling,
)


def test_string_googol():
    string = "googol"

    sa_naive = suffix_array_naive(string)
    sa_prefix_doubling = suffix_array_prefix_doubling(string)

    assert sa_naive == [6, 3, 0, 5, 2, 4, 1]
    assert sa_prefix_doubling == [6, 3, 0, 5, 2, 4, 1]
