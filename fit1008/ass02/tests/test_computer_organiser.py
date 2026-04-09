import unittest
from ed_utils.decorators import number

from computer import Computer
from computer_organiser import ComputerOrganiser


class TestComputerOrganiser(unittest.TestCase):

    @number("5.1")
    def test_example(self):
        c1 = Computer("c1", 2, 2, 0.1)
        c2 = Computer("c2", 9, 2, 0.2)
        c3 = Computer("c3", 6, 3, 0.3)
        c4 = Computer("c4", 1, 3, 0.4)
        c5 = Computer("c5", 6, 4, 0.5)
        c6 = Computer("c6", 3, 7, 0.6)
        c7 = Computer("c7", 7, 7, 0.7)
        c8 = Computer("c8", 8, 7, 0.8)
        c9 = Computer("c9", 6, 7, 0.9)
        c10 = Computer("c10", 4, 8, 1.0)

        co = ComputerOrganiser()
        co.add_computers([c1, c2])

        self.assertEqual([co.cur_position(m) for m in [c1, c2]], [0, 1])
        co.add_computers([c4, c3])
        self.assertEqual([co.cur_position(m) for m in [c1, c2, c3, c4]], [1, 3, 2, 0])
        co.add_computers([c5])
        self.assertEqual([co.cur_position(m) for m in [c1, c2, c3, c4, c5]], [1, 4, 2, 0, 3])
        co.add_computers([c7, c9, c6, c8])
        self.assertEqual([co.cur_position(m) for m in [c1, c2, c3, c4, c5, c6, c7, c8, c9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])

        self.assertRaises(KeyError, lambda: co.cur_position(c10))

    @number("5.2")
    def test_edge(self):
        """Not many edge cases. Try all in one."""
        co = ComputerOrganiser()
        self.assertRaises(KeyError, lambda: co.cur_position(Computer("test", 0, 0, 1)))
        c1, c2, c3, c4 = Computer("c1", 1, 1, 0.1), Computer("c2", 2, 2, 0.2), Computer("c3", 3, 3, 0.3), Computer("c4", 4, 4, 0.4)
        co.add_computers([c1, c2, c3, c4])
        self.assertEqual([co.cur_position(c) for c in [c1, c2, c3, c4]], [0, 1, 2, 3])

        # Test comparisons
        c5, c6, c7, c8, c9, c10 = Computer("b", 7, 0, 0.5), Computer("a", 7, 2, 0.6), Computer("c", 7, 1, 0.7), Computer("c", 8, 20, 0.8), Computer("b", 8, 2, 0.9), Computer("a", 8, 1, 1.0)
        co.add_computers([c5, c6, c7])
        co.add_computers([c8, c9, c10])
        self.assertEqual([co.cur_position(c) for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
