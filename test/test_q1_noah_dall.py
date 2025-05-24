import unittest
from crowded_campus import crowdedCampus

class TestQ1NoahDall(unittest.TestCase):
    def validate_allocation(self, n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation):
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)
        for a in allocation:
            self.assertTrue(0 <= a < m)
        counts = [0] * m
        for a in allocation:
            counts[a] += 1
        for j, (_, min_cap, max_cap) in enumerate(proposed_classes):
            self.assertTrue(min_cap <= counts[j] <= max_cap)
        satisfied = 0
        for i, a in enumerate(allocation):
            time_slot = proposed_classes[a][0]
            if time_slot in time_preferences[i][:5]:
                satisfied += 1
        self.assertGreaterEqual(satisfied, minimum_satisfaction)

    def test_trivial_single_student_single_class(self):
        n = 1
        m = 1
        time_preferences = [[0] + list(range(1, 20))]
        proposed_classes = [[0, 1, 1]]
        minimum_satisfaction = 1
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test_impossible_due_to_min_capacity(self):
        n = 3
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 2, 3], [1, 2, 3]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.assertIsNone(allocation)

    def test_exact_satisfaction_boundary(self):
        n = 5
        m = 2
        time_preferences = []
        for i in range(3):
            pref = [0] + [t for t in range(1, 20)]
            time_preferences.append(pref)
        for i in range(3, 5):
            pref = [1] + [t for t in range(2, 20)] + [0]
            time_preferences.append(pref)
        proposed_classes = [[0, 0, 3], [1, 0, 3]]
        minimum_satisfaction = 3
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test_capacity_and_time_constraints(self):
        n = 6
        m = 3
        time_preferences = []
        for group in [0, 0, 1, 1, 2, 2]:
            pref = [group] + [t for t in range(20) if t != group]
            time_preferences.append(pref)
        proposed_classes = [
            [0, 2, 2],
            [1, 2, 2],
            [2, 2, 2]
        ]
        minimum_satisfaction = 6
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test_parallel_classes_and_flexible_minimum(self):
        n = 10
        m = 2
        time_preferences = [[5] + [t for t in range(20) if t != 5] for _ in range(n)]
        proposed_classes = [[5, 0, 6], [5, 0, 6]]
        minimum_satisfaction = 10
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test_large_random_scenario(self):
        import random
        random.seed(1337)
        n = 50
        m = 5
        time_preferences = [random.sample(list(range(20)), 20) for _ in range(n)]
        proposed_classes = []
        for j in range(m):
            slot = j * 4
            min_cap = 5
            max_cap = 15
            proposed_classes.append([slot, min_cap, max_cap])
        minimum_satisfaction = 20
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        if allocation is not None:
            self.validate_allocation(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)
            
    def test_impossible_due_to_satisfaction_requirements(self):
        n = 5
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20))
        ]
        proposed_classes = [[19, 2, 3], [19, 2, 3]]
        minimum_satisfaction = 1
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.assertIsNone(allocation)

if __name__ == "__main__":
    unittest.main()