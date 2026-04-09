import unittest
from ed_utils.decorators import number

from computer import Computer
from route import Route, RouteSeries, RouteSplit


class TestRouteMethods(unittest.TestCase):

    @number("1.1")
    def test_example(self):
        """See spec for details"""
        a, b, c, d = (Computer(letter, 5, 5, 1.0) for letter in "abcd")

        empty = Route(None)

        series_b = RouteSeries(b, Route(RouteSeries(d, Route(None))))

        split = RouteSplit(
            Route(series_b),
            empty,
            Route(RouteSeries(c, Route(None)))
        )

        t = Route(RouteSeries(
            a,
            Route(split)
        ))

        res1 = series_b.add_empty_branch_after()
        self.assertIsInstance(res1, RouteSeries)
        self.assertEqual(res1.computer, b)
        self.assertIsInstance(res1.following.store, RouteSplit)
        self.assertEqual(res1.following.store.bottom.store, None)
        self.assertEqual(res1.following.store.top.store, None)
        self.assertIsInstance(res1.following.store.following.store, RouteSeries)
        self.assertEqual(res1.following.store.following.store.computer, d)
        self.assertEqual(res1.following.store.following.store.following.store, None)

        res2 = split.remove_branch()
        self.assertIsInstance(res2, RouteSeries)
        self.assertEqual(res2.computer, c)
        self.assertEqual(res2.following.store, None)

        res3 = empty.add_empty_branch_before()
        self.assertIsInstance(res3, Route)
        self.assertIsInstance(res3.store, RouteSplit)
        self.assertEqual(res3.store.bottom.store, None)
        self.assertEqual(res3.store.top.store, None)
        self.assertEqual(res3.store.following.store, None)

    @number("1.2")
    def test_empty(self):
        empty = Route(None)
        c = Computer("C", 1, 2, 1.0)

        res1 = empty.add_computer_before(c)

        self.assertIsInstance(res1, Route)
        self.assertIsInstance(res1.store, RouteSeries)
        self.assertEqual(res1.store.computer, c)
        self.assertEqual(res1.store.following.store, None)

        res2 = empty.add_empty_branch_before()
        self.assertIsInstance(res2, Route)
        self.assertIsInstance(res2.store, RouteSplit)
        self.assertEqual(res2.store.bottom.store, None)
        self.assertEqual(res2.store.top.store, None)
        self.assertEqual(res2.store.following.store, None)

    @number("1.3")
    def test_series(self):
        c = Computer("C", 3, 4, 0.1)
        empty = Route(None)
        series = RouteSeries(c, empty)

        c2 = Computer("I", 5, 6, 0.2)

        res1 = series.add_computer_after(c2)
        self.assertIsInstance(res1, RouteSeries)
        self.assertEqual(res1.computer, c)
        self.assertIsInstance(res1.following.store, RouteSeries)
        self.assertEqual(res1.following.store.computer, c2)

        res2 = series.add_computer_before(c2)
        self.assertIsInstance(res2, RouteSeries)
        self.assertEqual(res2.computer, c2)
        self.assertIsInstance(res2.following.store, RouteSeries)
        self.assertEqual(res2.following.store.computer, c)

        res3 = series.add_empty_branch_after()
        self.assertIsInstance(res3, RouteSeries)
        self.assertEqual(res3.computer, c)
        self.assertIsInstance(res3.following.store, RouteSplit)
        self.assertEqual(res3.following.store.bottom.store, None)
        self.assertEqual(res3.following.store.top.store, None)
        self.assertEqual(res3.following.store.following.store, None)

        res4 = series.add_empty_branch_before()
        self.assertIsInstance(res4, RouteSplit)
        self.assertEqual(res4.bottom.store, None)
        self.assertEqual(res4.top.store, None)
        self.assertIsInstance(res4.following.store, RouteSeries)
        self.assertEqual(res4.following.store.computer, c)

    @number("1.4")
    def test_split(self):
        m = Computer("C", 7, 8, 0.1)
        my_follow = RouteSeries(m, Route(None))
        t = RouteSplit(Route(None), Route(None), Route(my_follow))

        res = t.remove_branch()
        self.assertIsInstance(res, RouteSeries)
        self.assertEqual(res.computer, m)
        self.assertEqual(res.following.store, None)
