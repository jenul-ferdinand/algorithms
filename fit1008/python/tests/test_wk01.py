import pytest  # noqa
from wk01.ex01 import higher_lower
from wk01.ex02 import higher_lower as higher_lower2
from wk01.ex03 import binary_search
from wk01.ex04 import digital_root


def test_ex01():
    assert higher_lower(10, 20) == "higher"
    assert higher_lower(30, 10) == "lower"
    assert higher_lower(20, 20) == "correct"


def test_ex02(monkeypatch, capsys):
    inputs = iter(["15", "5", "10"])

    def mock_input(_):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError("Test finished - breaking input loop")

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    try:
        higher_lower2(10)
    except EOFError:
        pass

    captured = capsys.readouterr()
    assert "lower" in captured.out
    assert "higher" in captured.out
    assert "correct" in captured.out


def test_ex03():
    sarr = [1, 2, 3, 4, 5, 6, 7, 8, 10]

    assert binary_search(sarr, 1) == True
    assert binary_search(sarr, 10) == True
    assert binary_search(sarr, 5) == True
    assert binary_search(sarr, 12) == False


def test_ex04():
    assert digital_root(0) == 0
    assert digital_root(1) == 1
    assert digital_root(979853562951413) == 5