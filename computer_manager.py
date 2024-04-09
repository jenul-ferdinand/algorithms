from __future__ import annotations
from computer import Computer


class ComputerManager:

    def __init__(self) -> None:
        pass

    def add_computer(self, computer: Computer) -> None:
        raise NotImplementedError()

    def remove_computer(self, computer: Computer) -> None:
        raise NotImplementedError()

    def edit_computer(self, old: Computer, new: Computer) -> None:
        raise NotImplementedError()

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        raise NotImplementedError()

    def group_by_difficulty(self) -> list[list[Computer]]:
        raise NotImplementedError()
