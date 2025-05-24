import unittest
from typo import Bad_AI

class TestQ2EdwardYeung(unittest.TestCase):
    def test_bees(self):
        words = ['according', 'to', 'all', 'known', 'laws', 'of', 'aviation', 'there', 'is', 'no', 'way', 'a', 'bee', 'should', 'be', 'able', 'to', 'fly']
        input = ['acfording', 'tx', 'agl', 'khown', 'lass', 'ou', 'aviatzon', 'thyre', 'zs', 'qo', 'wak', 'l', 'vee', 'spould', 'bq', 'alle', 'ao', 'gly']

        ai = Bad_AI(list(set(words)))

        for i in range(len(input)):
            self.assertIn(words[i], ai.check_word(input[i]))

if __name__ == '__main__':
    unittest.main()