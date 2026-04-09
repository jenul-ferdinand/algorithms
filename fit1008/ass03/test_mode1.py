from unittest import TestCase
from ed_utils.decorators import number, visibility

from landsites import Land
from mode1 import Mode1Navigator


class Mode1Tests(TestCase):

    def load_basic(self):
        self.a = Land("A", 400, 100)
        self.b = Land("B", 300, 150)
        self.c = Land("C", 100, 5)
        self.d = Land("D", 350, 90)
        self.e = Land("E", 300, 100)
        # Create deepcopies of the sites
        self.sites = [
            Land(self.a.get_name(), self.a.get_gold(), self.a.get_guardians()),
            Land(self.b.get_name(), self.b.get_gold(), self.b.get_guardians()),
            Land(self.c.get_name(), self.c.get_gold(), self.c.get_guardians()),
            Land(self.d.get_name(), self.d.get_gold(), self.d.get_guardians()),
            Land(self.e.get_name(), self.e.get_gold(), self.e.get_guardians()),
        ]

    def check_solution(self, sites, starting_adv, solution, optimal):
        current_gold = 0
        current_adventurers = starting_adv
        for site, adventurers_sent in solution:
            self.assertGreaterEqual(adventurers_sent, 0)
            # This assertIn is written so that we allow copies with the same properties to be considered equal.
            self.assertIn((site.get_name(), site.get_gold(), site.get_guardians()), [(i.get_name(), i.get_gold(), i.get_guardians()) for i in sites])
            current_gold += min(site.get_gold() * adventurers_sent / site.get_guardians(), site.get_gold())
            current_adventurers -= adventurers_sent
            self.assertGreaterEqual(current_adventurers, 0)
        self.assertFalse(current_gold < optimal, "Your land selection is suboptimal!")
        if current_gold > optimal:
            raise ValueError("ERROR! You somehow made more gold than the intended solution1")

    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic(self):
        self.load_basic()
        nav = Mode1Navigator(self.sites, 200)
        selected = nav.select_sites()
        expected_gold = 865
        # ^ This can be achieved with ^
        # A: 100 adventurers
        # B: 0 adventurers
        # C: 5 adventurers
        # D: 90 adventurers
        # E: 5 adventurers
        self.check_solution(self.sites, 200, selected, expected_gold)
        # So we must be equal :)

    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_big_adventurers(self):
        self.load_basic()
        nav = Mode1Navigator(self.sites, 500)
        selected = nav.select_sites()
        expected_gold = 1450
        # ^ This can be achieved with ^
        # A: 100 guardians
        # B: 150 guardians
        # C: 5 guardians
        # D: 90 guardians
        # E: 100 guardians
        self.check_solution(self.sites, 500, selected, expected_gold)

    @number("1.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_no_adventurers(self):
        self.load_basic()
        nav = Mode1Navigator(self.sites, 0)
        selected = nav.select_sites()
        # If you did return any sites, you shouldn't have sent anyone.
        for site, adventuers_sent in selected:
            self.assertEqual(adventuers_sent, 0)

    @number("1.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_repeats(self):
        # choice function should not modify the outcome or the sites.
        self.load_basic()
        nav = Mode1Navigator(self.sites, 200)
        selected = nav.select_sites()
        selected_again = nav.select_sites()
        self.check_solution(self.sites, 200, selected, 865)
        self.check_solution(self.sites, 200, selected_again, 865)

    @number("1.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_updates(self):
        self.load_basic()
        nav = Mode1Navigator(self.sites, 200)
        selected = nav.select_sites()
        self.check_solution(self.sites, 200, selected, 865)
        # Update Land site A to have only 1 guardian, rather than 100.
        nav.update_site(self.sites[0], 400, 1)
        # Done for testing \/ so check_solution works.
        self.sites[0].set_guardians(1)
        selected_again = nav.select_sites()
        self.check_solution(self.sites, 200, selected_again, 1158)

    @number("1.6")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_multiple_adventures_sizes(self):
        self.load_basic()
        nav = Mode1Navigator(self.sites, 200)
        results = nav.select_sites_from_adventure_numbers([0, 200, 500, 300, 40])
        self.assertListEqual(results, [0, 865, 1450, 1160, 240])
