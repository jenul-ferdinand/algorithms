import unittest
from ed_utils.decorators import number

from computer import Computer
from route import Route, RouteSeries, RouteSplit
from virus import VirusType, TopVirus, BottomVirus, LazyVirus, RiskAverseVirus, FancyVirus, BranchDecision


class TestRouteMethods(unittest.TestCase):

    def load_example(self):
        self.top_top = Computer("top-top", 5, 3, 0.1)
        self.top_bot = Computer("top-bot", 3, 5, 0.2)
        self.top_mid = Computer("top-mid", 4, 7, 0.3)
        self.bot_one = Computer("bot-one", 2, 5, 0.4)
        self.bot_two = Computer("bot-two", 0, 0, 0.5)
        self.final   = Computer("final", 4, 4, 0.6)
        self.route = Route(RouteSplit(
            Route(RouteSplit(
                Route(RouteSeries(self.top_top, Route(None))),
                Route(RouteSeries(self.top_bot, Route(None))),
                Route(RouteSeries(self.top_mid, Route(None))),
            )),
            Route(RouteSeries(self.bot_one, Route(RouteSplit(
                Route(RouteSeries(self.bot_two, Route(None))),
                Route(None),
                Route(None),
            )))),
            Route(RouteSeries(self.final, Route(None)))
        ))

    def large_example(self):
        self.l_t_t_t_t = Computer("ttt", 5, 16, 0.1)
        self.l_t_t_t_b1 = Computer("ttb1", 5, 40, 0.2)
        self.l_t_t_t_b2 = Computer("ttb2", 5, 2, 0.3)
        self.l_t_t_t_x = Computer("ttx", 5, 12387, 0.4)
        self.l_t_t_b1 = Computer("tb1", 5, 5, 0.5)
        self.l_t_t_b2 = Computer("tb2", 5, 6, 0.6)
        self.l_t_t_b3 = Computer("tb3", 5, 7, 0.7)
        self.l_t_b1 = Computer("bb", 5, 0, 0.8)
        self.l_t_b2 = Computer("bb", 5, 12, 0.9)
        self.l_t1 = Computer("t1", 5, 14, 0)
        self.l_t2 = Computer("t2", 5, 19, 0.1)
        self.l_f = Computer("f", 5, 5, 0.2)
        self.l_x1 = Computer("x1", 5, 123, 0.3)
        self.l_x2 = Computer("x2", 5, 243, 0.4)
        self.l_b1 = Computer("lb1", 5, 1, 0.5)

        self.route = Route(RouteSeries(
            self.l_f,
            Route(RouteSplit(
                Route(RouteSeries(self.l_t1, Route(RouteSeries(self.l_t2, Route(RouteSplit(
                    Route(RouteSplit(
                        Route(RouteSplit(
                            Route(RouteSeries(self.l_t_t_t_t, Route(None))),
                            Route(RouteSeries(self.l_t_t_t_b1, Route(RouteSeries(self.l_t_t_t_b2, Route(None))))),
                            Route(RouteSeries(self.l_t_t_t_x, Route(None))),
                        )),
                        Route(RouteSeries(self.l_t_t_b1, Route(RouteSeries(self.l_t_t_b2, Route(RouteSeries(self.l_t_t_b3, Route(None))))))),
                        Route(None),
                    )),
                    Route(RouteSeries(self.l_t_b1, Route(RouteSeries(self.l_t_b2, Route(None))))),
                    Route(None),
                )))))),
                Route(RouteSeries(self.l_b1, Route(None))),
                Route(RouteSeries(self.l_x1, Route(RouteSeries(self.l_x2, Route(None))))),
            ))
        ))

    @number("2.1")
    def test_example(self):
        self.load_example()
        tw = TopVirus()
        bw = BottomVirus()
        lw = LazyVirus()
        self.route.follow_path(tw)
        self.route.follow_path(bw)
        self.route.follow_path(lw)

        self.assertListEqual(tw.computers, [self.top_top, self.top_mid, self.final])
        self.assertListEqual(bw.computers, [self.bot_one, self.final])
        self.assertListEqual(lw.computers, [self.top_bot, self.top_mid, self.final])

    @number("2.2")
    def test_risk_adverse_virus(self):
        self.large_example()
        rav = RiskAverseVirus()
        self.route.follow_path(rav)
        self.assertListEqual(rav.computers, [self.l_f, self.l_t1, self.l_t2, self.l_t_t_t_b1, self.l_t_t_t_b2,
                                             self.l_t_t_t_x, self.l_x1, self.l_x2])

    @number("2.3")
    def test_fancy_virus(self):
        self.load_example()
        fv = FancyVirus()
        FancyVirus.CALC_STR = "7 3 + 8 - 2 *"
        self.route.follow_path(fv)
        self.assertListEqual(fv.computers, [self.top_top, self.top_mid, self.final])

    @number("2.4")
    def test_custom_route(self):
        class CustomWalker(VirusType):
            def __init__(self) -> None:
                super().__init__()
                self.count = 0
                self.choices = [BranchDecision.BOTTOM, BranchDecision.STOP]
            def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
                self.count += 1
                return self.choices[self.count - 1]

        self.load_example()
        cw = CustomWalker()
        self.route.follow_path(cw)

        self.assertListEqual(cw.computers, [self.bot_one])

    @number("2.5")
    def test_collect_all_computers(self):
        self.load_example()
        res = self.route.add_all_computers()

        hash_computer = lambda m: m.name

        self.assertEqual(len(res), 6)
        self.assertSetEqual(set(map(hash_computer, res)), set(map(hash_computer, [
            self.top_bot, self.top_top, self.top_mid,
            self.bot_one, self.bot_two, self.final
        ])))
