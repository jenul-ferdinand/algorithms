from __future__ import annotations

from computer import Computer


class ComputerOrganiser:

    def __init__(self) -> None:
        raise NotImplementedError()

    def cur_position(self, computer: Computer) -> int:
        raise NotImplementedError()

    def add_computers(self, computers: list[Computer]) -> None:
        raise NotImplementedError()
