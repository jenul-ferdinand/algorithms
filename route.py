from __future__ import annotations
from dataclasses import dataclass
from computer import Computer
from typing import TYPE_CHECKING, Union
from branch_decision import BranchDecision

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:

    #    A split in the route.
    #       _____top______
    #      /              \
    #    -<                >-following-test
    #      \____bottom____/

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route."""
        return self.following.store


@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.
        """
        return self.following.store

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        return RouteSeries(computer, Route(self))

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        return RouteSeries(self.computer, Route(RouteSeries(computer, self.following)))

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current RouteStore is now the following path.
        """
        return RouteSplit(Route(None), Route(None), Route(self))

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        new_following = Route(RouteSplit(Route(None), Route(None), self.following))
        return RouteSeries(self.computer, new_following)


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:
    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """
        return Route(RouteSeries(computer, self))

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        return Route(RouteSplit(Route(None), Route(None), self))

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type."""
        current_route = self
        while current_route.store is not None:
            if isinstance(current_route.store, RouteSeries):
                # Add the computer in the series and move to the following route.
                virus_type.add_computer(current_route.store.computer)
                current_route = current_route.store.following
            elif isinstance(current_route.store, RouteSplit):
                # Decide which branch to take at the split.
                decision = virus_type.select_branch(current_route.store.top, current_route.store.bottom)
                if decision == BranchDecision.TOP:
                    current_route = current_route.store.top
                elif decision == BranchDecision.BOTTOM:
                    current_route = current_route.store.bottom
                else:  # BranchDecision.STOP
                    break  # If the decision is to stop, exit the loop.
                # Update current_route if it's still a RouteSplit
                if isinstance(current_route.store, RouteSplit):
                    current_route = current_route.store.following

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""

        def traverse(route_store):
            if route_store is None:
                return []
            elif isinstance(route_store, RouteSplit):
                return traverse(route_store.top.store) + traverse(route_store.bottom.store) + traverse(
                    route_store.following.store)
            elif isinstance(route_store, RouteSeries):
                return [route_store.computer] + traverse(route_store.following.store)
            return []

        return traverse(self.store)
