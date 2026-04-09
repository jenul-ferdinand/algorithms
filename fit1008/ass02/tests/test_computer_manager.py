import unittest
from ed_utils.decorators import number

from computer import Computer
from computer_manager import ComputerManager


class TestComputerManager(unittest.TestCase):

    @staticmethod
    def make_set(my_list: list) -> set:
        """
        Since computers are unhashable, add a method to get a set of all computer ids.
        Ensures that we can compare two lists without caring about order.
        """
        return set(id(x) for x in my_list)

    @number("6.1")
    def test_example(self):
        c1 = Computer("c1", 2, 2, 0.1)
        c2 = Computer("c2", 2, 9, 0.2)
        c3 = Computer("c3", 3, 6, 0.3)
        c4 = Computer("c4", 3, 1, 0.4)
        c5 = Computer("c5", 4, 6, 0.5)
        c6 = Computer("c6", 7, 3, 0.6)
        c7 = Computer("c7", 7, 7, 0.7)
        c8 = Computer("c8", 7, 8, 0.8)
        c9 = Computer("c9", 7, 6, 0.9)
        c10 = Computer("c10", 8, 4, 1.0)

        cm = ComputerManager()
        cm.add_computer(c1)
        cm.add_computer(c2)
        cm.add_computer(c3)
        cm.add_computer(c6)
        cm.add_computer(c7)

        self.assertEqual(self.make_set(cm.computers_with_difficulty(3)), self.make_set([c3]))
        self.assertEqual(self.make_set(cm.computers_with_difficulty(4)), self.make_set([]))
        self.assertEqual(self.make_set(cm.computers_with_difficulty(7)), self.make_set([c6, c7]))

        cm.add_computer(c4)
        cm.add_computer(c5)
        cm.add_computer(c8)
        cm.add_computer(c9)

        res = cm.group_by_difficulty()
        self.assertEqual(len(res), 4)
        self.assertEqual(self.make_set(res[0]), self.make_set([c1, c2]))
        self.assertEqual(self.make_set(res[1]), self.make_set([c3, c4]))
        self.assertEqual(self.make_set(res[2]), self.make_set([c5]))
        self.assertEqual(self.make_set(res[3]), self.make_set([c6, c7, c8, c9]))

        cm.add_computer(c10)
        cm.remove_computer(c5)

        res = cm.group_by_difficulty()
        self.assertEqual(len(res), 4)

        self.assertEqual(self.make_set(res[3]), self.make_set([c10]))

    @number("6.2")
    def test_example2(self):
        c1 = Computer("c1", 4, 4, 0.1)
        c2 = Computer("c2", 3, 2, 0.2)
        c3 = Computer("c3", 3, 5, 0.3)
        c4 = Computer("c4", 4, 3, 0.4)
        c5 = Computer("c5", 3, 4, 0.5)
        c6 = Computer("c6", 5, 3, 0.6)
        c7 = Computer("c7", 5, 3, 0.7)
        c8 = Computer("c8", 6, 4, 0.8)
        c9 = Computer("c9", 6, 4, 0.9)
        c10 = Computer("c10", 4, 5, 1.0)

        cm = ComputerManager()
        cm.add_computer(c1)
        cm.add_computer(c2)
        cm.add_computer(c3)
        cm.add_computer(c6)
        cm.add_computer(c7)

        self.assertEqual(self.make_set(cm.computers_with_difficulty(3)), self.make_set([c2, c3]))
        self.assertEqual(self.make_set(cm.computers_with_difficulty(4)), self.make_set([c1]))
        self.assertEqual(self.make_set(cm.computers_with_difficulty(7)), self.make_set([]))

        cm.add_computer(c4)
        cm.add_computer(c5)
        cm.add_computer(c8)
        cm.add_computer(c9)

        res = cm.group_by_difficulty()
        self.assertEqual(len(res), 4)

        self.assertEqual(self.make_set(res[0]), self.make_set([c2, c3, c5]))
        self.assertEqual(self.make_set(res[1]), self.make_set([c1, c4]))
        self.assertEqual(self.make_set(res[2]), self.make_set([c6, c7]))
        self.assertEqual(self.make_set(res[3]), self.make_set([c8, c9]))

        cm.add_computer(c10)
        cm.remove_computer(c9)

        res = cm.group_by_difficulty()
        self.assertEqual(len(res), 4)

        self.assertEqual(self.make_set(res[3]), self.make_set([c8]))
