import unittest
from fit2004.ass02.assignment2 import crowdedCampus, Bad_AI

class TestA2(unittest.TestCase):
    def validate_allocation(
        self, n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
    ):
        # Check correct type and length
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)

        # Class counts and satisfaction count
        counts = [0] * m
        satisfied = 0

        for i in range(n):
            class_id = allocation[i]
            self.assertTrue(0 <= class_id < m)
            counts[class_id] += 1
            time_slot = proposed_classes[class_id][0]
            if time_slot in time_preferences[i][:5]:
                satisfied += 1

        # Check class capacity constraints
        for j in range(m):
            min_cap, max_cap = proposed_classes[j][1], proposed_classes[j][2]
            self.assertGreaterEqual(counts[j], min_cap)
            self.assertLessEqual(counts[j], max_cap)

        # Check minimum satisfaction
        self.assertGreaterEqual(satisfied, minimum_satisfaction)

    def test_a_1(self):
        n, m = 1, 1
        time_preferences = [[0] + list(range(1, 20))]
        proposed_classes = [[0, 1, 1]]
        min_satisfaction = 1
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_2(self):
        n, m = 4, 2
        time_preferences = [[0] + list(range(1, 20))] * 4
        proposed_classes = [[0, 2, 2], [0, 2, 2]]
        min_satisfaction = 4
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_3(self):
        n, m = 3, 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 2, 3], [1, 2, 3]]
        min_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.assertIsNone(allocation)

    def test_a_4(self):
        n, m = 5, 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [1] + list(range(2, 20)) + [0],
            [1] + list(range(2, 20)) + [0],
        ]
        proposed_classes = [[0, 1, 3], [1, 1, 3]]
        min_satisfaction = 3
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_5(self):
        import random

        random.seed(42)
        n, m = 10, 3
        time_preferences = [random.sample(range(20), 20) for _ in range(n)]
        proposed_classes = [[0, 2, 4], [5, 2, 4], [10, 2, 4]]
        min_satisfaction = 5
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        if allocation:
            self.validate_allocation(
                n, m, time_preferences, proposed_classes, min_satisfaction, allocation
            )

    def test_a_6(self):
        n = 5
        m = 1
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 5, 5]]
        min_satisfaction = 5
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_7(self):
        n = 6
        m = 3
        time_preferences = [[j] + list(range(20)) for j in [0, 0, 1, 1, 2, 2]]
        proposed_classes = [[0, 2, 2], [1, 2, 2], [2, 2, 2]]
        min_satisfaction = 6
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_8(self):
        n = 4
        m = 2
        time_preferences = [[19, 18, 17, 16, 15] + list(range(15)) for _ in range(n)]
        proposed_classes = [[0, 2, 3], [1, 1, 2]]
        min_satisfaction = 4
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.assertIsNone(allocation)

    def test_a_9(self):
        n = 6
        m = 2
        time_preferences = [[5] + list(range(20)) for _ in range(n)]
        proposed_classes = [[5, 3, 3], [5, 3, 3]]
        min_satisfaction = 6
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_10(self):
        n = 4
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [1, 2] + list(range(2, 20)) + [0],
            [1, 2] + list(range(2, 20)) + [0],
            [2, 1] + list(range(3, 20)) + [0],
        ]
        proposed_classes = [[0, 1, 2], [1, 1, 2]]
        min_satisfaction = 2
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_g_1(self):
        n = 1
        m = 1
        prefs = [list(range(20))]
        classes = [[0, 1, 1]]
        min_sat = 1
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_2(self):
        n = 2
        m = 1
        prefs = [list(range(20))] * 2
        classes = [[0, 2, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_3(self):
        n = 2
        m = 2
        prefs = [[1, 0] + list(range(2, 20)), list(range(20))]
        classes = [[1, 1, 1], [0, 1, 1]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_4(self):
        n = 3
        m = 2
        prefs = [
            [0, 1] + list(range(2, 20)),
            [1, 0] + list(range(2, 20)),
            [0, 1] + list(range(2, 20)),
        ]
        classes = [[0, 2, 2], [1, 1, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_5(self):
        n = 4
        m = 2
        prefs = [[0, 1] + list(range(2, 20)) for _ in range(2)] + [
            [1, 0] + list(range(2, 20)) for _ in range(2)
        ]
        classes = [[0, 2, 2], [1, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_6(self):
        n = 3
        m = 2
        prefs = [list(range(20)) for _ in range(3)]
        classes = [[0, 1, 2], [0, 1, 2]]
        min_sat = 3
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_7(self):
        n = 4
        m = 2
        prefs = [list(range(20)) for _ in range(4)]
        classes = [[0, 2, 2], [0, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_j_1(self):
        n = 3
        m = 2
        time_preferences = [
            [0, 1, 2, 3, 4] + [t for t in range(20) if t not in [0, 1, 2, 3, 4]],
            [0, 1, 2, 3, 4] + [t for t in range(20) if t not in [0, 1, 2, 3, 4]],
            [1, 0, 2, 3, 4] + [t for t in range(20) if t not in [1, 0, 2, 3, 4]],
        ]
        proposed_classes = [[0, 2, 2], [1, 1, 2]]
        min_satisfaction = 2

        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_n_q1_1(self):
        n = 10
        m = 2
        time_preferences = [[5] + [t for t in range(20) if t != 5] for _ in range(n)]
        proposed_classes = [[5, 1, 6], [5, 1, 6]]
        minimum_satisfaction = 10
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
        )

    def test_n_q1_2(self):
        import random

        random.seed(1337)
        n = 50
        m = 5
        time_preferences = [random.sample(list(range(20)), 20) for _ in range(n)]
        proposed_classes = []
        for j in range(m):
            slot = j * 4
            min_cap = 5
            max_cap = 15
            proposed_classes.append([slot, min_cap, max_cap])
        minimum_satisfaction = 20
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        if allocation is not None:
            self.validate_allocation(
                n,
                m,
                time_preferences,
                proposed_classes,
                minimum_satisfaction,
                allocation,
            )

    def test_n_q1_3(self):
        n = 5
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
        ]
        proposed_classes = [[19, 2, 3], [19, 2, 3]]
        minimum_satisfaction = 1
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.assertIsNone(allocation)

    def test_n_q1_4(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 1, 4], [1, 1, 4]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.assertIsNone(allocation)

    def test_n_q1_5(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 5, 5], [1, 5, 5]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
        )

    def test_n_q2_1(self):
        ai = Bad_AI([])
        self.assertEqual(ai.check_word("any"), [])

    def test_n_q2_2(self):
        ai = Bad_AI(["", "a", "b"])
        self.assertEqual(ai.check_word(""), [])

    def test_n_q2_3(self):
        words = ["car", "cat", "bar"]
        ai = Bad_AI(words)
        result = ai.check_word("car")
        self.assertCountEqual(result, ["bar", "cat"])

    def test_n_q2_4(self):
        words = ["test", "best", "tent"]
        ai = Bad_AI(words)
        result = ai.check_word("test")
        self.assertCountEqual(result, ["best", "tent"])

    def test_n_q2_5(self):
        words = ["abcd", "abcf", "wxyz"]
        ai = Bad_AI(words)
        result = ai.check_word("abcd")
        self.assertEqual(result, ["abcf"])

    def test_n_q2_6(self):
        words = ["a", "ab", "abc"]
        ai = Bad_AI(words)
        self.assertEqual(ai.check_word("ab"), [])

    def test_n_q2_7(self):
        words = ["dog", "dig", "dag", "dot"]
        ai = Bad_AI(words)
        first = ai.check_word("dog")
        self.assertCountEqual(first, ["dig", "dag", "dot"])
        second = ai.check_word("dig")
        self.assertCountEqual(second, ["dog", "dag"])

    def test_bees(self):
        words = [
            "according",
            "to",
            "all",
            "known",
            "laws",
            "of",
            "aviation",
            "there",
            "is",
            "no",
            "way",
            "a",
            "bee",
            "should",
            "be",
            "able",
            "to",
            "fly",
        ]

        ai = Bad_AI(list(set(words)))
        input = [
            "acfording",
            "tx",
            "agl",
            "khown",
            "lass",
            "ou",
            "aviatzon",
            "thyre",
            "zs",
            "qo",
            "wak",
            "l",
            "vee",
            "spould",
            "bq",
            "alle",
            "ao",
            "gly",
        ]

        for i in range(len(input)):
            self.assertIn(words[i], ai.check_word(input[i]))

    def test_j_q2_1(self):
        words = ["aaa", "abc", "xyz", "aba", "aaaa"]
        ai = Bad_AI(words)

        sus_list = ["aaa", "axa", "ab", "xxx", "aaab"]
        expected = [["aba"], ["aaa", "aba"], [], [], ["aaaa"]]

        for sus, exp in zip(sus_list, expected):
            with self.subTest(sus_word=sus):
                result = ai.check_word(sus)
                self.assertCountEqual(result, exp)
                self.assertEqual(result, exp)

    def test_a_q2_1(self):
        ai = Bad_AI(["abc", "def", "ghi"])
        self.assertEqual(ai.check_word("xyz"), [])

    def test_a_q2_2(self):
        words = ["bake", "cake", "lake", "make"]
        ai = Bad_AI(words)
        result = ai.check_word("fake")
        self.assertCountEqual(result, ["bake", "cake", "lake", "make"])

    def test_a_q2_3(self):
        ai = Bad_AI(["hat", "bat", "cat"])
        result = ai.check_word("rat")
        self.assertCountEqual(result, ["hat", "bat", "cat"])

    def test_a_q2_4(self):
        ai = Bad_AI(["dog", "dot", "don"])
        result = ai.check_word("dop")
        self.assertCountEqual(result, ["dog", "dot", "don"])

    def test_a_q2_5(self):
        ai = Bad_AI(["hello", "hxllo", "hallo", "hillo"])
        result = ai.check_word("hello")
        self.assertCountEqual(result, ["hxllo", "hallo", "hillo"])

    def test_a_q2_6(self):
        ai = Bad_AI(["aaaa", "aaab", "aaba", "abaa", "baaa"])
        result = ai.check_word("aaaa")
        self.assertCountEqual(result, ["aaab", "aaba", "abaa", "baaa"])

    def test_a_q2_7(self):
        ai = Bad_AI(["word"])
        self.assertEqual(ai.check_word("word"), [])

    def test1g(self):
        n = 4
        m = 2
        time_preferences = [[0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20))]
        proposed_classes = [[0, 1, 20], [5, 3, 20]]
        min_satisfaction = 1
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, min_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, min_satisfaction, allocation)
        
    def test2g(self):
        n = 7
        m = 3
        time_preferences = [[0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20)),
                            [0] + list(range(1, 20))]

        proposed_classes = [[0, 1, 20], [0, 3, 5] ,[5, 3, 20]]
        min_satisfaction = 2
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, min_satisfaction)
        self.validate_allocation(n, m, time_preferences, proposed_classes, min_satisfaction, allocation)

if __name__ == "__main__":
    unittest.main()