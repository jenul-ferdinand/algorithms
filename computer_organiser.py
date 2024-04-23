from __future__ import annotations
from algorithms.binary_search import new_binary_search
from algorithms.mergesort import new_merge, new_mergesort
from computer import Computer
from data_structures.hash_table import LinearProbeTable
from infinite_hash_table import InfiniteHashTable


class ComputerOrganiser:

    def __init__(self) -> None:
        self.hash_table = LinearProbeTable()
        self.computers = []

    def cur_position(self, computer: Computer) -> int:
        if computer not in self.computers:
            raise KeyError(computer)
        position = new_binary_search(self.computers, computer)
        return position

    def add_computers(self, computers: list[Computer]) -> None:
        sorted_list = new_merge(new_mergesort(computers), self.computers)
        self.computers = sorted_list
    
if __name__ == '__main__':
    c1 = Computer("c1", 2, 2, 0.1)
    c2 = Computer("c2", 9, 2, 0.2)
    c3 = Computer("c3", 6, 3, 0.3)
    c4 = Computer("c4", 1, 3, 0.4)
    c5 = Computer("c5", 6, 4, 0.5)
    c6 = Computer("c6", 3, 7, 0.6)
    c7 = Computer("c7", 7, 7, 0.7)
    c8 = Computer("c8", 8, 7, 0.8)
    c9 = Computer("c9", 6, 7, 0.9)
    c10 = Computer("c10", 4, 8, 1.0)
    
    co = ComputerOrganiser()
    
    co.add_computers([c1, c2])
    assert([co.cur_position(m) for m in [c1, c2]] == [0, 1])
    
    co.add_computers([c4, c3])
    print(*[co.cur_position(m) for m in [c1, c2, c3, c4]])
    assert([co.cur_position(m) for m in [c1, c2, c3, c4]] == [1, 3, 2, 0])
