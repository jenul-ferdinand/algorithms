import unittest
from ed_utils.decorators import number

from double_key_table import DoubleKeyTable


class TestDoubleHash(unittest.TestCase):

    @number("3.1")
    def test_example(self):
        """
        See spec sheet image for clarification.
        """
        # Disable resizing / rehashing.
        class TestingDKT(DoubleKeyTable):
            def hash1(self, k):
                return ord(k[0]) % 12
            def hash2(self, k, sub_table):
                return ord(k[-1]) % 5

        dt = TestingDKT(sizes=[12], internal_sizes=[5])

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        self.assertRaises(KeyError, lambda: dt._linear_probe("May", "Jim", False))
        self.assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))
        dt["May", "Jim"] = 7 # Linear probing on internal table
        self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
        self.assertRaises(KeyError, lambda: dt._linear_probe("Het", "Liz", False))
        self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
        dt["Het", "Liz"] = 8 # Linear probing on external table
        self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))

    @number("3.2")
    def test_delete(self):
        # Disable resizing / rehashing.
        class TestingDKT(DoubleKeyTable):
            def hash1(self, k):
                return ord(k[0]) % 12
            def hash2(self, k, sub_table):
                return ord(k[-1]) % 5

        dt = TestingDKT(sizes=[12], internal_sizes=[5])

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["Tim", "Kat"] = 3

        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (0, 1))

        del dt["Tim", "Jen"]
        # We can't do this as it would create the table.
        # self.assertEqual(dt._linear_probe("Het", "Bob", True), (1, 3))
        del dt["Tim", "Kat"]
        # Deleting again should make space for Het.
        dt["Het", "Bob"] = 4
        self.assertEqual(dt._linear_probe("Het", "Bob", False), (0, 3))

        self.assertRaises(KeyError, lambda: dt._linear_probe("Tim", "Jen", False))
        dt["Tim", "Kat"] = 5
        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (1, 1))

    @number("3.3")
    def test_resize(self):
        class TestingDKT(DoubleKeyTable):
            def hash1(self, k):
                return ord(k[0]) % self.table_size
            def hash2(self, k, sub_table):
                return ord(k[-1]) % sub_table.table_size

        dt = TestingDKT(sizes=[3, 5], internal_sizes=[3, 5])

        dt["Tim", "Bob"] = 1
        # No resizing yet.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 2))
        dt["Tim", "Jen"] = 2
        # Internal resize.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 3))

        # External resize
        dt["Pip", "Bob"] = 4
        self.assertEqual(dt.table_size, 5)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (4, 3))
        self.assertEqual(dt._linear_probe("Pip", "Bob", False), (0, 2))

    @number("3.4")
    def test_keys_values(self):
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        dt["May", "Jim"] = 7
        dt["Het", "Liz"] = 8

        self.assertEqual(set(dt.keys()), {"Tim", "Amy", "May", "Ivy", "Het"})
        self.assertEqual(set(dt.keys("May")), {"Ben", "Tom", "Jim"})

        self.assertEqual(set(dt.values()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(dt.values("Tim")), {1, 6})

    @number("3.5")
    def test_iters(self):
        # Test that these are actually iterators,
        # and so changing the underlying data structure changes the next value.
        dt = DoubleKeyTable()
        dt["May", "Jim"] = 1
        dt["Kim", "Tim"] = 2

        key_iterator = dt.iter_keys()
        value_iterator = dt.iter_values()

        key = next(key_iterator)
        self.assertIn(key, ["May", "Kim"])
        value = next(value_iterator)
        self.assertIn(value, [1, 2])

        del dt["May", "Jim"]
        del dt["Kim", "Tim"]

        # Retrieving the next value should either raise StopIteration or crash entirely.
        # Note: Deleting from an element being iterated over is bad practice
        # We just want to make sure you aren't returning a list and are doing this
        # with an iterator.
        self.assertRaises(BaseException, lambda: next(key_iterator))
        self.assertRaises(BaseException, lambda: next(value_iterator))
