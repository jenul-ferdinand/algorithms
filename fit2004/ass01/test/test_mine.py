from fit2004.ass01.assignment1 import intercept
import unittest

class TestsByMe(unittest.TestCase):
    def test_circular_route_required(self):
        roads = [(0,1,5,1), (1,2,5,1), (2,3,5,1), (3,0,5,7)]
        stations = [(1,3), (3,5)]
        start = 0
        friend_start = 1

        self.assertEqual(intercept(roads, stations, start, friend_start), (15, 3, [0,1,2,3]))
        
    def test_no_valid_path(self):
        roads = [(0,1,5,2), (1,2,5,3), (2,0,5,4)]
        stations = [(3,2), (4,3)]
        start = 0
        friend_start = 3
        
        self.assertIsNone(intercept(roads, stations, start, friend_start))

if __name__ == '__main__':
  unittest.main()