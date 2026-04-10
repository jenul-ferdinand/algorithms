from fit3155.wk01.src.zalg import zalg


def test_repeating():
    assert zalg("aaaaaaa") == [7, 6, 5, 4, 3, 2, 1]


def test_nomatches():
    assert zalg("abcde") == [5, 0, 0, 0, 0]


def test_empty_string():
    assert zalg("") == []


def test_single():
    assert zalg("a") == [1]


def test_notes():
    assert zalg("aabcaabxaabcaabcay") == [
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
