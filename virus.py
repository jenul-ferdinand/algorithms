from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries, RouteSplit
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack


class VirusType(ABC):
    """
    Abstract base class for different types of virus behaviors in navigating and acting on a computer network.
    """

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        """
        Records a computer that the virus has passed through.

        :param computer: The computer to add to the list of visited computers.
        :type computer: Computer

        complexity best & worst: O(1)
        """
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Abstract method to decide which branch to take when encountering a split in the route.

        :param top_branch: The route object representing the top branch.
        :type top_branch: Route
        :param bottom_branch: The route object representing the bottom branch.
        :type bottom_branch: Route

        :return: The decision on which branch to take.
        :rtype: BranchDecision
        """
        pass


class TopVirus(VirusType):
    """
    A type of virus that always selects the top branch when encountering a split.
    """

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Always selects the top branch.

        :param top_branch: The route object representing the top branch.
        :type top_branch: Route
        :param bottom_branch: The route object representing the bottom branch.
        :type bottom_branch: Route

        :return: BranchDecision.TOP
        :rtype: BranchDecision

        complexity best & worst: O(1)
        """
        return BranchDecision.TOP


class BottomVirus(VirusType):
    """
    A type of virus that always selects the bottom branch when encountering a split.
    """

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Always selects the bottom branch.

        :param top_branch: The route object representing the top branch.
        :type top_branch: Route
        :param bottom_branch: The route object representing the bottom branch.
        :type bottom_branch: Route

        :return: BranchDecision.BOTTOM
        :rtype: BranchDecision

        complexity best & worst: O(1)
        """
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    """
    A type of virus that prefers the branch with the least hacking difficulty.
    """

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Selects the branch based on the least hacking difficulty of the first computer encountered in each branch.

        :param top_branch: The route object representing the top branch.
        :type top_branch: Route
        :param bottom_branch: The route object representing the bottom branch.
        :type bottom_branch: Route

        :return: Decision based on the comparison of hacking difficulty.
        :rtype: BranchDecision

        complexity best & worst: O(1)
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and prefers the path with the lowest risk factor.
        """
        is_top_series = isinstance(top_branch.store, RouteSeries)
        is_bottom_series = isinstance(bottom_branch.store, RouteSeries)

        if is_top_series and is_bottom_series:
            top_comp = top_branch.store.computer
            bottom_comp = bottom_branch.store.computer

            if top_comp.risk_factor == 0 and bottom_comp.risk_factor != 0:
                return BranchDecision.TOP
            elif top_comp.risk_factor != 0 and bottom_comp.risk_factor == 0:
                return BranchDecision.BOTTOM
            elif top_comp.risk_factor == 0 and bottom_comp.risk_factor == 0:
                if top_comp.hacking_difficulty < bottom_comp.hacking_difficulty:
                    return BranchDecision.TOP
                elif top_comp.hacking_difficulty > bottom_comp.hacking_difficulty:
                    return BranchDecision.BOTTOM

            top_val = max(top_comp.hacking_difficulty, int(top_comp.hacked_value / 2))
            bottom_val = max(bottom_comp.hacking_difficulty, int(bottom_comp.hacked_value / 2))

            if top_comp.risk_factor != 0 and bottom_comp.risk_factor != 0:
                top_val /= top_comp.risk_factor
                bottom_val /= bottom_comp.risk_factor

            if top_val < bottom_val:
                return BranchDecision.TOP
            elif bottom_val < top_val:
                return BranchDecision.BOTTOM

            if top_comp.risk_factor < bottom_comp.risk_factor:
                return BranchDecision.TOP
            elif top_comp.risk_factor > bottom_comp.risk_factor:
                return BranchDecision.BOTTOM
            elif top_comp.risk_factor == bottom_comp.risk_factor:
                return BranchDecision.STOP

        if not is_top_series and is_bottom_series:
            return BranchDecision.TOP
        elif is_top_series and not is_bottom_series:
            return BranchDecision.BOTTOM

        return BranchDecision.STOP


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"  # This should correctly calculate to a meaningful value.

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:

        is_top_split = isinstance(top_branch.store, RouteSplit)
        is_bottom_split = isinstance(bottom_branch.store, RouteSplit)

        if is_top_split and not is_bottom_split:
            return BranchDecision.TOP
        elif not is_top_split and is_bottom_split:
            return BranchDecision.BOTTOM

        threshold = self.evaluate_rpn(self.CALC_STR)
        top_comp = top_branch.store.computer
        bottom_comp = bottom_branch.store.computer

        if top_comp.hacked_value < threshold:
            return BranchDecision.TOP
        elif bottom_comp.hacked_value > threshold:
            return BranchDecision.BOTTOM
        elif not top_comp.hacked_value < threshold and not bottom_comp.hacked_value > threshold:
            return BranchDecision.STOP

        return BranchDecision.TOP

    @staticmethod
    def evaluate_rpn(expression):
        """Evaluate a reverse polish notation expression"""
        stack = []
        for token in expression.split():
            if token in '+-*/':
                b, a = stack.pop(), stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
            else:
                stack.append(float(token))
        return stack[0] if stack else 0


if __name__ == "__main__":
    top_top = Computer("top-top", 5, 3, 0.1)
    top_bot = Computer("top-bot", 3, 5, 0.2)
    top_mid = Computer("top-mid", 4, 7, 0.3)
    bot_one = Computer("bot-one", 2, 5, 0.4)
    bot_two = Computer("bot-two", 0, 0, 0.5)
    final = Computer("final", 4, 4, 0.6)

    route = Route(RouteSplit(
        Route(RouteSplit(
            Route(RouteSeries(top_top, Route(None))),
            Route(RouteSeries(top_bot, Route(None))),
            Route(RouteSeries(top_mid, Route(None))),
        )),
        Route(RouteSeries(bot_one, Route(RouteSplit(
            Route(RouteSeries(bot_two, Route(None))),
            Route(None),
            Route(None),
        )))),
        Route(RouteSeries(final, Route(None)))
    ))

    # Instantiate viruses
    tw = TopVirus()
    bw = BottomVirus()
    lw = LazyVirus()
    rav = RiskAverseVirus()
    fv = FancyVirus()
    FancyVirus.CALC_STR = "7 3 + 8 - 2 *"

    # Define a function to format computer details for output
    def format_computer_details(computers):
        return "[\n" + ",\n".join(f"  Computer(name='{comp.name}', "
                                  f"hacking_difficulty={comp.hacking_difficulty}, "
                                  f"hacked_value={comp.hacked_value}, "
                                  f"risk_factor={comp.risk_factor})" for comp in computers) + "\n]"


    # Run viruses through the route
    route.follow_path(tw)
    route.follow_path(bw)
    route.follow_path(lw)
    route.follow_path(rav)
    route.follow_path(fv)

    # Print results
    print("Testing TopVirus:")
    print("Computers visited by TopVirus:", format_computer_details(tw.computers))

    print("\nTesting BottomVirus:")
    print("Computers visited by BottomVirus:", format_computer_details(bw.computers))

    print("\nTesting LazyVirus:")
    print("Computers visited by LazyVirus:", format_computer_details(lw.computers))

    print("\nTesting RiskAverseVirus:")
    print("Computers visited by RiskAverseVirus:", format_computer_details(rav.computers))

    print("\nTesting FancyVirus:")
    print("Computers visited by FancyVirus:", format_computer_details(fv.computers))
