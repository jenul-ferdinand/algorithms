import unittest
from assignment2 import Bad_AI

class TestQ2NoahDall(unittest.TestCase):
    def test1(self):
        ai = Bad_AI([])
        self.assertEqual(ai.check_word("any"), [])

    def test2(self):
        ai = Bad_AI(["", "a", "b"])
        self.assertEqual(ai.check_word(""), [])

    def test3(self):
        words = ["car", "cat", "bar"]
        ai = Bad_AI(words)
        result = ai.check_word("car")
        self.assertCountEqual(result, ["bar", "cat"])

    def test4(self):
        words = ["test", "best", "tent"]
        ai = Bad_AI(words)
        result = ai.check_word("test")
        self.assertCountEqual(result, ["best", "tent"])

    def test5(self):
        words = ["abcd", "abcf", "wxyz"]
        ai = Bad_AI(words)
        result = ai.check_word("abcd")
        self.assertEqual(result, ["abcf"])

    def test6(self):
        words = ["a", "ab", "abc"]
        ai = Bad_AI(words)
        self.assertEqual(ai.check_word("ab"), [])

    def test7(self):
        words = ["dog", "dig", "dag", "dot"]
        ai = Bad_AI(words)
        first = ai.check_word("dog")
        self.assertCountEqual(first, ["dig", "dag", "dot"])
        second = ai.check_word("dig")
        self.assertCountEqual(second, ["dog", "dag"])

if __name__ == '__main__':
    unittest.main()