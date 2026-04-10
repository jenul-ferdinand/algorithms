from fit3155.wk01.src.naive import naive

def test_one_letter():
    assert naive("a") == [1]


def test_repeating():
    assert naive("aaaaaaa") == [7, 6, 5, 4, 3, 2, 1]
