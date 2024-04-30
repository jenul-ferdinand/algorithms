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
        while current_route and current_route.store:
            if isinstance(current_route.store, RouteSeries):
                print(f"{virus_type.__class__.__name__} visiting: {current_route.store.computer.name}")
                virus_type.add_computer(current_route.store.computer)
                current_route = current_route.store.following
            elif isinstance(current_route.store, RouteSplit):
                print(f"{virus_type.__class__.__name__} at a split: deciding between top and bottom routes.")
                decision = virus_type.select_branch(current_route.store.top, current_route.store.bottom)
                print(f"{virus_type.__class__.__name__} decision: {decision}")
                if decision == BranchDecision.TOP:
                    current_route = current_route.store.top
                elif decision == BranchDecision.BOTTOM:
                    current_route = current_route.store.bottom
                else:
                    print(f"{virus_type.__class__.__name__} stopped at the split.")
                    break
            if current_route and not isinstance(current_route.store, (RouteSeries, RouteSplit)):
                print(f"{virus_type.__class__.__name__} reached end of path segment")
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
