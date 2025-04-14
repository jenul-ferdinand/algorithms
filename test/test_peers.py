from assignment1 import intercept
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
        
    def test_loop_finish(self):
        roads = [(1,5,2,1),(1,6,11,6),(2,5,6,3),(3,7,1,10),(4,2,4,1),(5,3,8,8),(5,4,20,2),(5,1,4,1),(6,2,9,6),(7,6,15,2)]
        stations = [(1,3),(2,3),(3,5)]
        start = 1
        friend_start = 2

        self.assertEqual(intercept(roads, stations, start, friend_start), (24, 8, [1,5,1,5,1,5,1,5,1]))
    
    def test_station_chase(self):
        roads = [(1,2,2,1),(1,3,50,2),(2,3,3,2),(3,4,5,2),(3,5,15,3),(4,5,1,2),(5,2,4,1)]
        stations = [(1,1),(2,2),(3,2),(4,2),(5,1)]
        start = 1
        friend_start = 2

        self.assertEqual(intercept(roads, stations, start, friend_start), (15, 8, [1,2,3,4,5,2]))
    
    def test_equal_costs(self):
        roads = [(1,2,3,3),(2,5,1,1),(3,4,5,2),(3,1,11,4),(3,2,10,7),(3,5,5,7),(4,1,5,2),(5,2,5,7)]
        stations = [(1,3),(2,4)]
        start = 3
        friend_start = 2

        self.assertEqual(intercept(roads, stations, start, friend_start), (10, 4, [3,4,1]))
    
    def test_valid_path(self):
        roads = [(1,5,1,1),(2,5,4,2),(3,2,3,3),(3,4,2,1),(4,2,1,1),(5,1,5,1)]
        stations = [(1,2),(2,3)]
        start = 3
        friend_start = 1

        self.assertEqual(intercept(roads, stations, start, friend_start), (3,2,[3,4,2]))
        
    def test_repeatedV2(self):
        roads = [(0, 1, 20, 3), (1, 2, 10, 2), (2, 0, 15, 4), (0, 3, 50, 2), (3, 4, 10, 1), (4, 5, 10, 1), (5, 6, 10, 1), (6, 1, 30, 2)]
        stations = [(3, 2), (6, 1), (1, 4)]   
        start = 0
        friendStart = 6

        self.assertEqual(intercept(roads, stations, start, friendStart), (125, 14, [0, 1, 2, 0, 3, 4, 5, 6]))
        
    def test_long_chase(self):
        import sys
        rec_lim = sys.getrecursionlimit()
        sys.setrecursionlimit(2000)
        roads = [(i, i+1, 3, 5) for i in range(19)] + [(19, 0, 3, 4)]
        stations = [(i, 5) for i in range(20)]
        start = 0
        friend_start = 19

        #1900 edges traversed/95 cycles
        self.assertEqual(intercept(roads, stations, start, friend_start), (5700, 9405, [i for i in range(20)]*95+[0]))
        sys.setrecursionlimit(rec_lim)

if __name__ == '__main__':
  unittest.main()