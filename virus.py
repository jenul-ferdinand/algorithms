from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries
from branch_decision import BranchDecision


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
        This virus is risk averse and likes to choose the path with the lowest risk factor.
        """

        def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
            # Check if both branches have computers (are RouteSeries)
            top_series = isinstance(top_branch.store, RouteSeries)
            bottom_series = isinstance(bottom_branch.store, RouteSeries)

            # Function to calculate the score for comparison
            def calculate_score(computer):
                # Avoid division by zero in case risk factor is 0
                value = max(computer.hacking_difficulty, computer.hacked_value / 2)
                return value / computer.risk_factor if computer.risk_factor else float('inf')

            if top_series and bottom_series:
                top_computer = top_branch.store.computer
                bottom_computer = bottom_branch.store.computer

                # Check for computers with zero risk factor
                if top_computer.risk_factor == 0.0 and bottom_computer.risk_factor == 0.0:
                    # Choose the path with the lower hacking difficulty
                    return BranchDecision.TOP if top_computer.hacking_difficulty <= bottom_computer.hacking_difficulty \
                        else BranchDecision.BOTTOM
                elif top_computer.risk_factor == 0.0:
                    return BranchDecision.TOP
                elif bottom_computer.risk_factor == 0.0:
                    return BranchDecision.BOTTOM

                # Compute scores for each path
                top_score = calculate_score(top_computer)
                bottom_score = calculate_score(bottom_computer)

                # Compare the scores
                if top_score > bottom_score:
                    return BranchDecision.TOP
                elif top_score < bottom_score:
                    return BranchDecision.BOTTOM
                else:
                    # Tiebreaker with the lower risk factor
                    if top_computer.risk_factor < bottom_computer.risk_factor:
                        return BranchDecision.TOP
                    elif top_computer.risk_factor > bottom_computer.risk_factor:
                        return BranchDecision.BOTTOM
                    else:
                        return BranchDecision.STOP

            # If one branch is a RouteSeries and the other a RouteSplit, pick RouteSplit
            if top_series and not bottom_series:
                return BranchDecision.BOTTOM
            elif not top_series and bottom_series:
                return BranchDecision.TOP

            # In all other cases, default to the top path
            return BranchDecision.TOP


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.
        """
        # Compute the threshold by evaluating CALC_STR
        threshold = self.evaluate_rpn(self.CALC_STR)

        # Check if both branches have computers
        top_series = isinstance(top_branch.store, RouteSeries)
        bottom_series = isinstance(bottom_branch.store, RouteSeries)

        if top_series and bottom_series:
            # Compare hacked_value with the threshold
            if top_branch.store.computer.hacked_value < threshold:
                return BranchDecision.TOP
            elif bottom_branch.store.computer.hacked_value > threshold:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        elif top_series or bottom_series:
            # If only one branch has a RouteSeries, pick RouteSplit
            return BranchDecision.BOTTOM if top_series else BranchDecision.TOP

        # In all other cases, default to the top path
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
