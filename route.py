from __future__ import annotations
from dataclasses import dataclass
from computer import Computer
from typing import TYPE_CHECKING, Union
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack

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
        current_path = self.store
        path_stack = LinkedStack()
        path_stack.push(current_path)

        while not path_stack.is_empty():
            current_path = path_stack.pop()

            if isinstance(current_path, RouteSeries):
                virus_type.add_computer(current_path.computer)
                if current_path.following.store is not None:
                    path_stack.push(current_path.following.store)
                elif path_stack.is_empty():
                    break
                else:
                    path_stack.push(path_stack.pop().following.store)

            elif isinstance(current_path, RouteSplit):
                path_stack.push(current_path)
                decision = virus_type.select_branch(current_path.top, current_path.bottom)

                if decision == BranchDecision.TOP:
                    path_stack.push(current_path.top.store)
                elif decision == BranchDecision.BOTTOM:
                    path_stack.push(current_path.bottom.store)
                elif decision == BranchDecision.STOP:
                    break

            elif current_path is None:
                if path_stack.is_empty():
                    break
                else:
                    path_stack.push(path_stack.pop().following.store)

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
