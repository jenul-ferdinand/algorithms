import unittest
from ed_utils.decorators import number

from infinite_hash_table import InfiniteHashTable


class TestInfiniteHash(unittest.TestCase):

    @number("4.1")
    def test_example(self):
        ih = InfiniteHashTable()
        ih["lin"] = 1
        ih["leg"] = 2
        self.assertEqual(ih.get_location("lin"), [4, 1])
        self.assertEqual(ih.get_location("leg"), [4, 23])
        self.assertEqual(len(ih), 2)
        ih["mine"] = 3
        ih["linked"] = 4
        self.assertEqual(ih.get_location("mine"), [5])
        self.assertEqual(ih.get_location("lin"), [4, 1, 6, 26])
        self.assertEqual(ih.get_location("linked"), [4, 1, 6, 3])
        self.assertEqual(len(ih), 4)
        ih["limp"] = 5
        ih["mining"] = 6
        self.assertEqual(ih.get_location("limp"), [4, 1, 5])
        self.assertEqual(ih.get_location("mine"), [5, 1, 6, 23])
        self.assertEqual(ih.get_location("mining"), [5, 1, 6, 1])
        self.assertEqual(len(ih), 6)
        ih["jake"] = 7
        ih["linger"] = 8
        self.assertEqual(ih.get_location("jake"), [2])
        self.assertEqual(ih.get_location("linger"), [4, 1, 6, 25])
        self.assertEqual(len(ih), 8)

    @number("4.2")
    def test_delete(self):
        ih = InfiniteHashTable()
        ih["lin"] = 1
        ih["leg"] = 2
        ih["mine"] = 3
        ih["linked"] = 4
        ih["limp"] = 5
        ih["mining"] = 6
        ih["jake"] = 7
        ih["linger"] = 8

        del ih["limp"]

        # Should do nothing
        self.assertEqual(ih.get_location("linked"), [4, 1, 6, 3])

        del ih["mine"]

        self.assertEqual(ih.get_location("mining"), [5])
        self.assertRaises(KeyError, lambda: ih.get_location("mine"))

        del ih["mining"]
        del ih["jake"]
        del ih["leg"]
        del ih["linger"]
        del ih["linked"]

        self.assertEqual(ih["lin"], 1)
        self.assertEqual(ih.get_location("lin"), [4])

        del ih["lin"]

        ih["lin"] = 10
        self.assertEqual(ih.get_location("lin"), [4])
        self.assertEqual(len(ih), 1)

    @number("4.3")
    def test_sort_keys(self):
        ih = InfiniteHashTable()
        ih["lin"] = 1
        ih["leg"] = 2
        ih["mine"] = 3
        ih["linked"] = 4
        ih["limp"] = 5
        ih["mining"] = 6
        ih["jake"] = 7
        ih["linger"] = 8
        res = ih.sort_keys()
        expected = [
            "jake",
            "leg",
            "limp",
            "lin",
            "linger",
            "linked",
            "mine",
            "mining"
        ]
        self.assertListEqual(res, expected)
