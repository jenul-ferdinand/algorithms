from fit2004.ass02.assignment2 import crowdedCampus
import unittest

class TestQ1GavinChandra(unittest.TestCase):
    def test1z(self):
        n = 6
        m = 2
        time_preferences = [list(range(0, 20))] * 6
        proposed_classes = [[0, 5, 10], [5, 1, 10]]
        minimum_satisfaction = 6
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.assertIsNone(allocation)
        
if __name__ == '__main__':
    unittest.main()