from assignment2 import crowdedCampus
from helpers import make_full_prefs, make_full_prefs_random
import unittest

class TestQ1Basic(unittest.TestCase):
    def single_student_and_class(self):
        res = crowdedCampus(
            num_students = 1, 
            num_classes = 1, 
            time_prefs = [
                list(range(20)) # Student 0 prefers all classes
            ], 
            classes = [
                [0,1,1] # Class at time 0, min students 1, max students 1
            ], 
            min_satis = 1
        )
        ans = [0] # Student 0 is assigned to class 0
            
        self.assertEqual(res, ans)
        
    def test_two_students_one_class_both_satisfied(self):
        res = crowdedCampus(
            num_students=2,
            num_classes=1,
            time_prefs=[
                make_full_prefs([0]), 
                make_full_prefs([0])
            ],
            classes=[
                [0, 2, 2]
            ],
            min_satis=1
        )
        self.assertEqual(res, [0, 0])

    def test_unattainable_satisfaction(self):
        res = crowdedCampus(
            num_students=2,
            num_classes=1,
            time_prefs=[
                [1, 0, 2, 3, 4] + list(range(5, 20)),
                [1, 0, 2, 3, 4] + list(range(5, 20))
            ],
            classes=[
                [5, 2, 2]
            ],
            min_satis=2
        )
        self.assertIsNone(res)

    def test_higher_threshold_satisfaction(self):
        res = crowdedCampus(
            num_students=2,
            num_classes=1,
            time_prefs=[
                [1, 0, 2, 3, 4] + list(range(5, 20)),
                [1, 0, 2, 3, 4] + list(range(5, 20))
            ],
            classes=[[0, 2, 2]],
            min_satis=2
        )
        self.assertEqual(res, [0, 0])

    def test_two_students_two_classes_exact_matching(self):
        res = crowdedCampus(
            num_students=2,
            num_classes=2,
            time_prefs=[
                make_full_prefs([0, 1, 2, 3, 4]),
                make_full_prefs([1, 0, 2, 3, 4])
            ],
            classes=[[0, 1, 1], [1, 1, 1]],
            min_satis=2
        )
        self.assertEqual(res, [0, 1])

    def test_three_students_two_classes_mixed(self):
        res = crowdedCampus(
            num_students=3,
            num_classes=2,
            time_prefs=[
                make_full_prefs([0, 1, 2, 3, 4]),
                make_full_prefs([0, 1, 2, 3, 4]),
                make_full_prefs([1, 0, 2, 3, 4])
            ],
            classes=[
                [0, 2, 2], 
                [1, 1, 2]
            ],
            min_satis=2
        )
        self.assertEqual(res, [0, 0, 1])

    def test_infeasible_min_greater_than_students(self):
        res = crowdedCampus(
            num_students=1,
            num_classes=1,
            time_prefs=[
                [5, 0, 1, 2, 3] + list(range(6, 20))
            ],
            classes=[
                [5, 2, 2]
            ],
            min_satis=0
        )
        self.assertIsNone(res)
        
if __name__ == '__main__':
    unittest.main()