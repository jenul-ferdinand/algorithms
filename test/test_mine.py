from intercept import intercept
import unittest

class TestsByMe(unittest.TestCase):
    def test_multiple_equally_optimal_solutions(self):
        roads = [(0,1,10,5), (0,2,10,5), (1,3,5,2), (2,3,5,2), (3,4,7,3)]
        stations = [(3,2), (4,3)]
        start = 0
        friend_start = 3

        self.assertEqual(intercept(roads, stations, start, friend_start), (15,7,[0,1,3]) or (15,7,[0,2,3]))

    def test_long_train_loop(self):
        roads = [(0,1,5,2), (1,2,6,3), (2,3,7,4), (3,4,8,5), (4,5,9,6), (5,6,10,7), (6,7,11,8), (7,0,12,9)]
        stations = [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
        start = 0
        friend_start = 1

        self.assertEqual(intercept(roads, stations, start, friend_start), (5,2,[0,1]))

    def test_just_making_it(self):
        roads = [(0,1,10,10), (1,2,5,3), (2,3,5,3), (3,4,5,3)]
        stations = [(4,5), (2,4)]
        start = 0
        friend_start = 4

        self.assertEqual(intercept(roads, stations, start, friend_start), (25, 19, [0,1,2,3,4]))

    def test_circular_route_required(self):
        roads = [(0,1,5,1), (1,2,5,1), (2,3,5,1), (3,0,5,7)]
        stations = [(1,3), (3,7)]
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