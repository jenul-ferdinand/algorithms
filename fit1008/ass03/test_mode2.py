from unittest import TestCase
from ed_utils.decorators import number, visibility

from landsites import Land

from mode2 import Mode2Navigator


class Mode2Tests(TestCase):

    def load_basic(self):
        self.a = Land("A", 400, 100)
        self.b = Land("B", 300, 150)
        self.c = Land("C", 100, 5)
        self.d = Land("D", 350, 90)
        self.e = Land("E", 300, 100)
        self.sites = [
            self.a, self.b, self.c, self.d, self.e
        ]

    @number("2.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_day(self):
        self.load_basic()

        # Used later
        cur_guardians = {
            site.get_name(): site.get_guardians()
            for site in self.sites
        }
        cur_gold = {
            site.get_name(): site.get_gold()
            for site in self.sites
        }

        nav = Mode2Navigator(8)
        nav.add_sites(self.sites)
        results = nav.simulate_day(100)

        # The first team makes 400 gold by going to land site A and sending 100 their adventurers.
        # Final score: 400 + 0*2.5 = 400
        # The second team makes 375 gold by going to land site D and sending 90 of their adventurers.
        # Final score: 350 + 10*2.5 = 375
        # The third team makes 337.5 gold by going to land site C and sending 5 of their adventurers.
        # Final score: 100 + 95*2.5 = 337.5
        # The fourth team makes 300 gold by going to land site E and sending 100 of their adventurers.
        # Final score: 300 + 0*2.5 = 300
        # The fifth, sixth, seventh, eighth teams should end up with 250 gold.
        expected_scores = [400, 375, 337.5, 300, 250, 250, 250, 250]
        self.assertEqual(len(results), len(expected_scores))

        for (site, sent_adventurers), expected in zip(results, expected_scores):
            
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold = cur_gold[site.get_name()]
            guardians = cur_guardians[site.get_name()]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_adventurers / guardians)
            # Update site
            cur_gold[site.get_name()] = gold - received
            cur_guardians[site.get_name()] = max(0, guardians - sent_adventurers)
            # Score
            score = 2.5 * (100 - sent_adventurers) + received
            self.assertEqual(score, expected)

    @number("2.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_add_again(self):
        
        self.load_basic()

        # Used later
        cur_guardians = {
            site.get_name(): site.get_guardians()
            for site in self.sites
        }
        cur_gold = {
            site.get_name(): site.get_gold()
            for site in self.sites
        }

        nav = Mode2Navigator(3)
        nav.add_sites(self.sites)
        results_1 = nav.simulate_day(100)
        # Same first 3 decisions as test 2.1
        expected_1 = [400, 375, 337.5]
        self.assertEqual(len(results_1), len(expected_1))
        
        for (site, sent_adventurers), expected in zip(results_1, expected_1):
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold = cur_gold[site.get_name()]
            guardians = cur_guardians[site.get_name()]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_adventurers / guardians)
            # Update Site
            cur_gold[site.get_name()]      = gold - received
            cur_guardians[site.get_name()] = max(0, guardians - sent_adventurers)
            # Score
            score = 2.5 * (100 - sent_adventurers) + received
            self.assertEqual(score, expected)
        nav.add_sites([Land("F", 900, 150)])
        cur_guardians["F"] = 150
        cur_gold["F"] = 900
        results_2 = nav.simulate_day(100)
        # The first 2 teams on this day can plunder land site F, after which the same decisions as in test 2.1 continue
        expected_2 = [600, 425, 300]
        self.assertEqual(len(results_2), len(expected_2))
        for (site, sent_adventurers), expected in zip(results_2, expected_2):
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold      = cur_gold[site.get_name()]
            guardians = cur_guardians[site.get_name()]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_adventurers / guardians)
            # Update Site
            cur_gold[site.get_name()] = gold - received
            cur_guardians[site.get_name()] = max(0, guardians - sent_adventurers)
            # Score
            score = 2.5 * (100 - sent_adventurers) + received
            self.assertEqual(score, expected)
