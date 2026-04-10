from fit2004.ass02.assignment2 import crowdedCampus
from fit2004.ass02.helpers import make_full_prefs
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