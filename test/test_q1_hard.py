from crowded_campus import crowdedCampus
from helpers import make_full_prefs, make_full_prefs_random
import unittest

class TestQ1Hard(unittest.TestCase):
    def test_hard_case(self):
        res = crowdedCampus(
            num_students = 3,
            num_classes = 3,
            min_satis = 0,
            classes = [
                [0, 1, 1],
                [1, 1, 1],
                [2, 1, 1]
            ],
            time_prefs = [
                make_full_prefs([10]),
                make_full_prefs([11]),
                make_full_prefs([12])
            ]
        )
        self.assertEqual(res, [0, 1, 2])