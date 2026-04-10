from __future__ import annotations
from fit1008.ass02.algorithms.binary_search import binary_search
from fit1008.ass02.algorithms.mergesort import merge, mergesort
from fit1008.ass02.computer import Computer
from fit1008.ass02.data_structures.hash_table import LinearProbeTable
from fit1008.ass02.infinite_hash_table import InfiniteHashTable

__author__ = "Jenul Ferdinand 33119805"

class ComputerOrganiser:

    def __init__(self) -> None:
        self.computers = []

    def cur_position(self, computer: Computer) -> int:
        """Gets the current position of the computer

        :param computer: The computer to search
        :type computer: Computer
        :raises KeyError: When the the computer is not found in the list
        :return: The position of the target computer
        :rtype: int
        
        :complexity best: O(N) occurs when the target element is the central element in the list, but we still have to iterate and check if the computer is not in the list, N is the length of self.computers.
        :complexity worst: O(N * logN) occurs when the target element is positioned in the extremities (first or last) of the the sorted list. 
        """
        pos = binary_search(self.computers, computer)
        if pos < 0 or pos > len(self.computers)-1: raise KeyError('Computer is out of bounds')
        if self.computers[pos] is not computer: raise KeyError('Computer does not exist')
        return pos

    def add_computers(self, computers: list[Computer]) -> None:
        """Adds a computer to the computer list sorted based on the computers hacking_difficulty -> risk_factor -> name in ascending order.

        :param computers: The list of computers to add to
        :type computers: list[Computer]
        
        :complexity best and worst: O(NlogN + M), where N is the length of the input list 'computers' and M is the total length of the resulting merged list. Merging is linear with respect to the total number of items in the two lists being merged.
        """
        self.computers = merge(mergesort(computers), self.computers)
    
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
