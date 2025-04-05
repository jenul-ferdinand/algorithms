from intercept import intercept
import unittest

class TestsFromSpec(unittest.TestCase):
    def test_simple(self):
        roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
                    (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
                    (3,2,15,2), (9,3,2,2), (2,4,10,5)]
        stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
        start = 6
        friend_start = 0

        self.assertEqual(intercept(roads, stations, start, friend_start), (7, 9, [6,7,8,3]))

    def test_unsolvable(self):
        roads = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), (4,1,22,2),
                    (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
        stations = [(4,3), (5,2), (3,4)]
        start = 0
        friend_start = 4

        self.assertIsNone(intercept(roads, stations, start, friend_start))

    def test_repeated(self):
        roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3),
                    (1,5,60,4), (5,3,70,2), (3,0,10,7)]
        stations = [(4,2), (5,1), (3,4)]
        start = 0
        friendStart = 3

        self.assertEqual(intercept(roads, stations, start, friendStart), (160, 39, [0,1,2,0,1,2,0,4]))

    def test_samecost_difftime(self):
        roads = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
        stations = [(2,4), (1,3)]
        start = 0
        friendStart = 1

        self.assertEqual(intercept(roads, stations, start, friendStart), (10, 3, [0,2]))

if __name__ == '__main__':
  unittest.main()