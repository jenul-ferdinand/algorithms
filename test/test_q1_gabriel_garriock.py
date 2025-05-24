from crowded_campus import crowdedCampus
from helpers import make_full_prefs, make_full_prefs_random
import unittest

class TestQ1GabrielGarriock(unittest.TestCase):
    def test_gabriel_case1(self):
        res = crowdedCampus(
            num_students=1,
            num_classes=1,
            time_prefs=[
                make_full_prefs([])
            ],
            classes=[
                [0, 1, 1]
            ],
            min_satis=1
        )
        self.assertEqual(res, [0])

    def test_gabriel_case2(self):
        res = crowdedCampus(
            num_students=2,
            num_classes=1,
            time_prefs=[
                make_full_prefs([]), 
                make_full_prefs([])
            ],
            classes=[
                [0, 2, 2]
            ],
            min_satis=2
        )
        self.assertEqual(res, [0, 0])
        
    def test_gabriel_case3(self):
        res = crowdedCampus(
            2,
            2,
            [
                [1,0] + list(range(2,20)),
                list(range(20))
            ],
            [
                [1,1,1],
                [0,1,1]
            ],
            2
        )
        self.assertEqual(res, [0,1])
        
    def test_gabriel_case4(self):
        res = crowdedCampus(
            3, 
            2,
            [
                [0,1] + list(range(2,20)),
                [1,0] + list(range(2,20)),
                [0,1] + list(range(2,20))
            ],
            [
                [0,2,2],
                [1,1,2]
            ],
            3
        )
        self.assertEqual(res, [0,1,0])
        
    def test_gabriel_case5(self):
        res = crowdedCampus(
            4,
            2,
            [[0, 1] + list(range(2, 20)) for _ in range(2)]
            + [[1, 0] + list(range(2, 20)) for _ in range(2)],
            [
                [0,2,2],
                [1,2,2]
            ],
            4
        )
        self.assertEqual(res, [0, 0, 1, 1])
        
    def test_gabriel_case6(self):
        res = crowdedCampus(
            3, 2,
            [list(range(20)) for _ in range(3)],
            [[0, 1, 2], [0, 1, 2]],
            3
        )
        self.assertEqual(res, [0,0,1])
        
    def test_gabriel_case7(self):
        res = crowdedCampus(
            4, 2,
            [list(range(20)) for _ in range(4)],
            [[0, 2, 2], [0, 2, 2]],
            4
        )
        self.assertEqual(res, [0,0,1,1])