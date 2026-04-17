from fit3155.wk03.src.bwt import bwt


def test_simple():
    string = "banana$"

    b = bwt(string)
    b_naive = bwt(string)

    answer = "annb$aa"

    assert b == answer
    assert b_naive == answer
