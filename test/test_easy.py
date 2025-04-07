from intercept import intercept
import unittest

class SimpleTestCases(unittest.TestCase):
    def test_linear_path(self):
        """
        * A straight path, driver must travel along a linear road 0->1->2->3->4
        
        ! There is also a bad shortcut from 1->4 which will give too high of a
        ! cost, even though it has a time of 0 to travel.
        !  The driver should skip this "bad shortcut".
        
        # [images/test_linear_path.png]
        """
        roads = [(0,1,5,2), (1,2,5,2), (2,3,5,2), (3,4,5,2), (1,4,30,2)]
        stations = [(4,2), (2,2)]
        start = 0
        friend_start = 4
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (20, 8, [0,1,2,3,4]))

    def test_branch_choice(self):
        """
        * Need to choose between two paths, one clearly better than the other
        
        ! The driver must choose to take the shortcut from 1->4.
        ! This shortcut has both better cost & time compared to 1->2->3->4.
        
        # [images/test_branch_choice.png]
        """
        # Need to choose between two paths, one clearly better than the other
        roads = [(0,1,5,2), (1,2,5,2), (2,3,5,2), (3,4,5,2), (1,4,14,2)]
        stations = [(4,2), (2,2)]
        start = 0
        friend_start = 4
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (19,4,[0,1,4]))

    def test_small_loop(self):
        # A simple circular path where optimal choice is obvious
        roads = [(0,1,5,2), (1,2,5,2), (2,3,5,2), (3,0,15,6)]
        stations = [(2,1), (0,1)]
        start = 0
        friend_start = 2
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (10, 4, [0,1,2]))

    def test_bidirectional_roads(self):
        # Tests roads going both directions between locations
        roads = [(0,1,5,2), (1,0,4,2), (1,2,5,2), (2,1,4,2)]
        stations = [(0,3), (2,2)]
        start = 1
        friend_start = 0
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (4, 2, [1,0]))

    def test_star_configuration(self):
        # Central hub with multiple spokes
        roads = [(0,1,5,1), (0,2,6,2), (0,3,7,3), (0,4,8,4), 
                 (1,0,5,1), (2,0,6,2), (3,0,7,3), (4,0,8,4)]
        stations = [(0,1), (2,2), (4,3)]
        start = 1
        friend_start = 0
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (23, 7, [1, 0, 2, 0, 2]))

    def test_edge_case_just_in_time(self):
        # Arriving at a station at exactly the right time to intercept
        roads = [(0,1,10,10), (1,2,5,3), (2,3,5,3), (3,4,5,3)]
        stations = [(4,5), (2,4)]
        start = 0
        friend_start = 4
        
        self.assertEqual(intercept(roads, stations, start, friend_start), 
                         (25, 19, [0,1,2,3,4]))

    def test_equal_cost_paths(self):
        # Multiple paths with the same cost but different times
        roads = [(0,1,10,5), (0,2,10,5), (1,3,5,2), (2,3,5,2)]
        stations = [(3,2)]
        start = 0
        friend_start = 3
        
        # Either path is valid as they have equal cost
        result = intercept(roads, stations, start, friend_start)
        self.assertEqual(result[0], 15)  # Cost should be 15
        self.assertEqual(result[1], 7)   # Time should be 7
        # Path can be either [0,1,3] or [0,2,3]

if __name__ == '__main__':
    unittest.main()