from __future__ import annotations
from dataclasses import dataclass
from computer import Computer
from typing import TYPE_CHECKING, Union
from branch_decision import BranchDecision

if TYPE_CHECKING:
    from virus import VirusType

@dataclass
class RouteSplit:
    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        print(f"Removing branch, leaving following route.")
        return self.following.store

@dataclass
class RouteSeries:
    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        print(f"Removing computer: {self.computer.name}")
        return self.following.store

    def add_computer_before(self, computer: Computer) -> RouteStore:
        print(f"Adding computer before current: {computer.name}")
        return RouteSeries(computer, Route(self))

    def add_computer_after(self, computer: Computer) -> RouteStore:
        print(f"Adding computer after current: {computer.name}")
        return RouteSeries(self.computer, Route(RouteSeries(computer, self.following)))

    def add_empty_branch_before(self) -> RouteStore:
        print("Adding an empty branch before the current route.")
        return RouteSplit(Route(None), Route(None), Route(self))

    def add_empty_branch_after(self) -> RouteStore:
        print("Adding an empty branch after the current computer.")
        new_following = Route(RouteSplit(Route(None), Route(None), self.following))
        return RouteSeries(self.computer, new_following)

RouteStore = Union[RouteSplit, RouteSeries, None]

@dataclass
class Route:
    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        print(f"Adding computer before everything: {computer.name}")
        return Route(RouteSeries(computer, self))

    def add_empty_branch_before(self) -> Route:
        print("Adding an empty branch before everything.")
        return Route(RouteSplit(Route(None), Route(None), self))

    def follow_path(self, virus_type: VirusType) -> None:
        print(f"Starting path traversal for {virus_type.__class__.__name__}")
        current_route = self
        decision_stack = []  # Stack to keep track of decisions for backtracking

        while current_route and current_route.store:
            if isinstance(current_route.store, RouteSeries):
                print(f"{virus_type.__class__.__name__} visiting: {current_route.store.computer.name}")
                virus_type.add_computer(current_route.store.computer)
                current_route = current_route.store.following
            elif isinstance(current_route.store, RouteSplit):
                if decision_stack and decision_stack[-1][0] == current_route:
                    # We are backtracking to a previously visited split
                    _, decision_made = decision_stack.pop()
                    if decision_made == BranchDecision.TOP:
                        # Now try the bottom route if not tried
                        current_route = current_route.store.bottom
                        print(f"{virus_type.__class__.__name__} backtracking: choosing bottom route")
                    else:
                        # All options exhausted, continue backtracking
                        continue
                else:
                    # Decide which branch to take at the split
                    decision = virus_type.select_branch(current_route.store.top, current_route.store.bottom)
                    decision_stack.append((current_route, decision))
                    print(f"{virus_type.__class__.__name__} at a split: decision {decision}")
                    if decision == BranchDecision.TOP:
                        current_route = current_route.store.top
                    elif decision == BranchDecision.BOTTOM:
                        current_route = current_route.store.bottom
                    else:
                        print(f"{virus_type.__class__.__name__} stopping at split.")
                        break

        while decision_stack:
            # Continue backtracking if there's more to explore
            current_route, decision_made = decision_stack.pop()
            if decision_made == BranchDecision.TOP:
                current_route = current_route.store.bottom
                print(f"{virus_type.__class__.__name__} backtracking: choosing bottom route")
            else:
                continue  # No more paths to backtrack

            # Resume traversal from the new current route
            while current_route and current_route.store:
                if isinstance(current_route.store, RouteSeries):
                    print(f"{virus_type.__class__.__name__} visiting: {current_route.store.computer.name}")
                    virus_type.add_computer(current_route.store.computer)
                    current_route = current_route.store.following
                elif isinstance(current_route.store, RouteSplit):
                    decision = virus_type.select_branch(current_route.store.top, current_route.store.bottom)
                    decision_stack.append((current_route, decision))
                    print(f"{virus_type.__class__.__name__} at a split: decision {decision}")
                    if decision == BranchDecision.TOP:
                        current_route = current_route.store.top
                    elif decision == BranchDecision.BOTTOM:
                        current_route = current_route.store.bottom
                    else:
                        print(f"{virus_type.__class__.__name__} stopping at split.")
                        break

        print(f"{virus_type.__class__.__name__} completed path traversal.")

    def add_all_computers(self) -> list[Computer]:
        computers = []

        def traverse(route_store):
            if isinstance(route_store, RouteSeries):
                computers.append(route_store.computer)
                traverse(route_store.following.store)
            elif isinstance(route_store, RouteSplit):
                traverse(route_store.top.store)
                traverse(route_store.bottom.store)
                traverse(route_store.following.store)

        traverse(self.store)
        return computers
