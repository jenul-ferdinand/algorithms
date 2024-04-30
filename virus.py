from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries, RouteSplit
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack


class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        """Add a computer that the virus has passed through."""
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Selects between the top and bottom branch during a route traversal.

        Parameters:
        top_branch (Route): The route object representing the top branch.
        bottom_branch (Route): The route object representing the bottom branch.

        Returns:
        BranchDecision: The decision on which branch to take.
        """
        pass


class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the top branch
        return BranchDecision.TOP


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the bottom branch
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.
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
        # Get the first computer on each route if exists
        top_comp = getattr(top_branch.store, 'computer', None) if isinstance(top_branch.store, RouteSeries) else None
        bot_comp = getattr(bottom_branch.store, 'computer', None) if isinstance(bottom_branch.store,
                                                                                RouteSeries) else None

        # Decision logic based on computer risk factors
        if top_comp and bot_comp:
            # Compare risk factors directly
            if top_comp.risk_factor < bot_comp.risk_factor:
                return BranchDecision.TOP
            elif top_comp.risk_factor > bot_comp.risk_factor:
                return BranchDecision.BOTTOM
        elif top_comp:  # Only top route has a computer
            return BranchDecision.TOP
        elif bot_comp:  # Only bottom route has a computer
            return BranchDecision.BOTTOM

        # Default to stopping if both routes are equivalent or both are None
        return BranchDecision.STOP


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"  # This should correctly calculate to a meaningful value.

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        threshold = self.evaluate_rpn(FancyVirus.CALC_STR)
        top_comp = self.safe_get_computer(top_branch)
        bot_comp = self.safe_get_computer(bottom_branch)

        if top_comp and bot_comp:
            top_diff = abs(top_comp.hacked_value - threshold)
            bot_diff = abs(bot_comp.hacked_value - threshold)
            if top_diff < bot_diff:
                return BranchDecision.TOP
            else:
                return BranchDecision.BOTTOM
        elif top_comp:
            return BranchDecision.TOP
        elif bot_comp:
            return BranchDecision.BOTTOM
        return BranchDecision.STOP

    def safe_get_computer(self, branch: Route):
        """ Safely retrieve the computer from a branch if it exists. """
        if branch and branch.store and isinstance(branch.store, RouteSeries):
            return branch.store.computer
        return None

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
                    stack.append(a / b if b != 0 else float('inf'))  # Handle division by zero
            else:
                stack.append(float(token))
        return stack.pop() if stack else 0


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

