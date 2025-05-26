from assignment2 import crowdedCampus
from helpers import make_full_prefs, make_full_prefs_random
import unittest

class TestQ1Overfill(unittest.TestCase):
    def test_overfill_phase2a(self):
        res = crowdedCampus(
            num_students=3,
            num_classes=1,
            time_prefs=[
                make_full_prefs_random([10, 11, 12, 13, 14]),
                make_full_prefs_random([10, 11, 12, 13, 14]),
                make_full_prefs_random([0, 1, 2, 3, 4])
            ],
            classes=[
                [0, 2, 2]
            ],
            min_satis=1
        )
        self.assertIsNone(res)

    def test_multiclass_overfill_interaction(self):
        res = crowdedCampus(
            num_students=4,
            num_classes=2,
            time_prefs=[
                make_full_prefs([10]),
                make_full_prefs([11]),
                make_full_prefs([12]),
                make_full_prefs([0])
            ],
            classes=[
                [0, 2, 2], 
                [1, 1, 1]
            ],
            min_satis=1
        )
        self.assertIsNone(res)

    def test_min_force_filling_phase2b_overfills(self):
        res = crowdedCampus(
            num_students=3,
            num_classes=1,
            time_prefs=[
                make_full_prefs([10]),
                make_full_prefs([11]),
                make_full_prefs([12])
            ],
            classes=[
                [0, 2, 2]
            ],
            min_satis=0
        )
        self.assertIsNone(res)

    def test_min_barely_met_max_overfill(self):
        res = crowdedCampus(
            num_students=3,
            num_classes=1,
            time_prefs=[
                make_full_prefs([10]),
                make_full_prefs([11]),
                make_full_prefs([12])
            ],
            classes=[
                [0, 1, 2]
            ],
            min_satis=0
        )
        self.assertIsNone(res)
