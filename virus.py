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
        # Calculate threshold from RPN to ensure it is executed and calculate correctly.
        threshold = self.evaluate_rpn(FancyVirus.CALC_STR)
        print(f"Threshold calculated: {threshold}")

        # Safely retrieve computers from both top and bottom branches
        top_comp = self.safe_get_computer(top_branch)
        bot_comp = self.safe_get_computer(bottom_branch)
        print(f"Top computer: {top_comp}, Bottom computer: {bot_comp}")

        if top_comp and bot_comp:
            # Decide based on which computer's hacked value is closer to the threshold
            top_diff = abs(top_comp.hacked_value - threshold)
            bot_diff = abs(bot_comp.hacked_value - threshold)

            if top_diff < bot_diff:
                return BranchDecision.TOP
            elif bot_diff < top_diff:
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
    # Create some sample computers and routes for testing
    comp1 = Computer("Comp1", hacking_difficulty=5, hacked_value=10, risk_factor=0.1)
    comp2 = Computer("Comp2", hacking_difficulty=3, hacked_value=15, risk_factor=0.2)
    comp3 = Computer("Comp3", hacking_difficulty=4, hacked_value=5, risk_factor=0.05)
    comp4 = Computer("Comp4", hacking_difficulty=2, hacked_value=20, risk_factor=0.3)

    # Setup routes
    route_top = Route(RouteSeries(comp1, Route(None)))
    route_bottom = Route(RouteSeries(comp2, Route(None)))
    route_following = Route(RouteSeries(comp3, Route(RouteSeries(comp4, Route(None)))))

    # Create a split route
    split_route = Route(RouteSplit(route_top, route_bottom, route_following))

    # Initialize viruses
    top_virus = TopVirus()
    bottom_virus = BottomVirus()
    lazy_virus = LazyVirus()
    risk_averse_virus = RiskAverseVirus()
    fancy_virus = FancyVirus()

    # Define a helper function to format computer details
    def format_computer_details(computers):
        return "[\n" + ",\n".join(f"  Computer(name='{comp.name}', "
                                  f"hacking_difficulty={comp.hacking_difficulty}, "
                                  f"hacked_value={comp.hacked_value}, "
                                  f"risk_factor={comp.risk_factor})" for comp in computers) + "\n]"


    # Testing each virus and printing formatted output
    viruses = [("TopVirus", top_virus), ("BottomVirus", bottom_virus),
               ("LazyVirus", lazy_virus), ("RiskAverseVirus", risk_averse_virus),
               ("FancyVirus", fancy_virus)]

    for virus_name, virus in viruses:
        split_route.follow_path(virus)
        print(f"\nTesting {virus_name}:")
        formatted_output = format_computer_details(virus.computers)
        print(f"Computers visited by {virus_name}: {formatted_output}")

