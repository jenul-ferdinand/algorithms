import unittest
from assignment2 import Bad_AI

class TestQ2Mine(unittest.TestCase):
    def test_spec_examples(self):
        words = ['aaa', 'abc', 'xyz', 'aba', 'aaaa']
        ai = Bad_AI(words)

        sus_list = ['aaa', 'axa', 'ab', 'xxx', 'aaab']
        expected = [
            ['aba'],        # 'aaa' → ['aba']
            ['aaa', 'aba'], # 'axa' → ['aaa','aba']
            [],             # 'ab'  → []
            [],             # 'xxx' → []
            ['aaaa']        # 'aaab'→ ['aaaa']
        ]

        for sus, exp in zip(sus_list, expected):
            with self.subTest(sus_word=sus):
                result = ai.check_word(sus)
                # Order doesn’t matter
                self.assertCountEqual(result, exp)
                # Order does matter
                # self.assertEqual(result, exp)
                
    def test_axple(self):
        # sus_word_2 = "axple"  # Expect ["apple","axply"]
        words = ["apple", "apply", "axply", "apricot", "banana"]
        ai = Bad_AI(words)
        res = ai.check_word("axple")
        self.assertCountEqual(res, ["apple", "axply"])

    def test_apxly(self):
        # sus_word_3 = "apxly"  # Expect ["apply"]
        words = ["apple", "apply", "axply", "apricot", "banana"]
        ai = Bad_AI(words)
        res = ai.check_word("apxly")
        self.assertEqual(res, ["apply"])

    def test_apricots_length_mismatch(self):
        # sus_word_4 = "apricots"  # Expect []
        words = ["apple", "apply", "axply", "apricot", "banana"]
        ai = Bad_AI(words)
        res = ai.check_word("apricots")
        self.assertEqual(res, [])

    def test_axxyz_no_match(self):
        # sus_word_5 = "axxyz"  # Expect []
        words = ["apple", "apply", "axply", "apricot", "banana"]
        ai = Bad_AI(words)
        res = ai.check_word("axxyz")
        self.assertEqual(res, [])

    def test_cot(self):
        # sus_word_3_1 = "cot"  # Expect ["cat","cog"]
        words = ["cat", "bat", "cot", "cog", "dog"]
        ai = Bad_AI(words)
        res = ai.check_word("cot")
        self.assertCountEqual(res, ["cat", "cog"])


if __name__ == '__main__':
    unittest.main()