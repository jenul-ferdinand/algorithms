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
        This virus is risk averse and likes to choose the path with the lowest risk factor.
        """

        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:

            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.risk_factor == 0 and bot_comp.risk_factor != 0:
                return BranchDecision.TOP
            elif top_comp.risk_factor != 0 and bot_comp.risk_factor == 0:
                return BranchDecision.BOTTOM
            elif top_comp.risk_factor == 0 and bot_comp.risk_factor == 0:
                if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                    return BranchDecision.TOP
                elif bot_comp.hacking_difficulty < top_comp.hacking_difficulty:
                    return BranchDecision.BOTTOM

            top_val = max(int(top_comp.hacking_difficulty), int(top_comp.hacked_value / 2))
            bot_val = max(int(bot_comp.hacking_difficulty), int(bot_comp.hacked_value / 2))

            if top_comp.risk_factor != 0 and bot_comp.risk_factor != 0:
                top_val /= top_comp.risk_factor
                bot_val /= bot_comp.risk_factor

            if top_val < bot_val:
                return BranchDecision.TOP
            elif bot_val < top_val:
                return BranchDecision.BOTTOM

            if top_comp.risk_factor < bot_comp.risk_factor:
                return BranchDecision.TOP
            elif top_comp.risk_factor > bot_comp.risk_factor:
                return BranchDecision.BOTTOM
            elif top_comp.risk_factor == bot_comp.risk_factor:
                return BranchDecision.STOP

            if not top_route and bot_route:
                return BranchDecision.TOP
            elif top_route and not bot_route:
                return BranchDecision.BOTTOM

            return BranchDecision.TOP


from data_structures.linked_stack import LinkedStack


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.
        """
        top_route = isinstance(top_branch.store, RouteSplit)
        bot_route = isinstance(bottom_branch.store, RouteSplit)

        if top_route and not bot_route:
            return BranchDecision.TOP
        elif not top_route and bot_route:
            return BranchDecision.BOTTOM

        threshold = self.solve_notation(self.CALC_STR)
        top_comp = top_branch.store.following.store.computer
        bot_comp = bottom_branch.store.following.store.computer

        if top_comp.hacked_value < threshold:
            return BranchDecision.TOP
        elif bot_comp.hacked_value > threshold:
            return BranchDecision.BOTTOM
        else:
            return BranchDecision.STOP

    def solve_notation(self, to_solve: str) -> float:
        """Evaluate a reverse polish notation expression"""
        solver_stack = LinkedStack()

        for item in to_solve.split():
            if item.isdigit():
                solver_stack.push(float(item))
            else:
                op2 = solver_stack.pop()
                op1 = solver_stack.pop()
                if item == '+':
                    result = op1 + op2
                elif item == '-':
                    result = op1 - op2
                elif item == '*':
                    result = op1 * op2
                elif item == '/':
                    result = op1 / op2
                solver_stack.push(result)
        return solver_stack.peek()

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

