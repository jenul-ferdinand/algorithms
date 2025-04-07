from intercept import intercept
import unittest

class PeerTestCases(unittest.TestCase):
    def test_1(self):
        roads = [(0, 2, 10, 3), (1, 2, 5, 2), (2, 1, 15, 5), (2, 0, 12, 10)]
        stations = [(0, 5), (1, 5)]
        start = 2
        friendStart = 0
        expected_output = (12, 10, [2, 0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_2(self):
        stations_input = [(i, 2) for i in range(20)]
        start_input = 20
        friendStart_input = 0
        roads_input = [(20, 2, 7, 4), (20, 18, 30, 36)] + \
                      [(i, (i+1)%20, 1, 2) for i in range(20)]
        expected_output = (7, 4, [20, 2])
        result = intercept(roads_input, stations_input, start_input, friendStart_input)
        self.assertEqual(result, expected_output)

    def test_3(self):
        stations_input = [(i, 5) for i in range(20)]
        start_input = 20
        friendStart_input = 0
        roads_input = [(20, 5, 30, 25), (20, 0, 40, 100)] + \
                      [(i, (i+1)%20, 1, 1) for i in range(20)]
        expected_output = (30, 25, [20, 5])
        result = intercept(roads_input, stations_input, start_input, friendStart_input)
        self.assertEqual(result, expected_output)

    def test_4(self):
        roads = [(0, 1, 1, 1), (1, 0, 1, 1),
                 (2, 3, 1, 1), (3, 2, 1, 1)]
        stations = [(0, 5), (1, 5)]
        start = 2
        friendStart = 0
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test_5(self):
        roads = [(0, 1, 10, 3), (1, 2, 20, 10), (2, 0, 8, 4)]
        stations = [(0, 5), (1, 5), (2, 5)]
        start = 1
        friendStart = 0
        expected_output = (20, 10, [1, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)
        
    def test_case_set2(self):
        a = [1,2,3,4,5,6,7,8,9,10,11,12]
        stations = [(4,3), (5,3), (6,3)]
        start = 1
        friendStart = 6
        roads = [None] * len(a)
        for number in a:
            roads[number-1] = [(1,2,1,3), (2,3,1,3), (3,1,1,3), (1,4,1,number), (4,5,1,3), (5,6,1,3), (6,4,1,3)]

        self.assertIsNone(intercept(roads[0], stations, start, friendStart))
        self.assertIsNone(intercept(roads[1], stations, start, friendStart))
        self.assertEqual(intercept(roads[2], stations, start, friendStart), (1, 3, [1,4]))
        self.assertIsNone(intercept(roads[3], stations, start, friendStart))
        self.assertIsNone(intercept(roads[4], stations, start, friendStart))
        self.assertIsNone(intercept(roads[5], stations, start, friendStart))
        self.assertIsNone(intercept(roads[6], stations, start, friendStart))
        self.assertIsNone(intercept(roads[7], stations, start, friendStart))
        self.assertIsNone(intercept(roads[8], stations, start, friendStart))
        self.assertIsNone(intercept(roads[9], stations, start, friendStart))
        self.assertIsNone(intercept(roads[10], stations, start, friendStart))
        self.assertEqual(intercept(roads[11], stations, start, friendStart), (1, 12, [1,4]))

if __name__ == '__main__':
  unittest.main()