from __future__ import annotations
from fit1008.ass02.algorithms.mergesort import mergesort
from fit1008.ass02.computer import Computer
from fit1008.ass02.data_structures.hash_table import LinearProbeTable

__author__ = "Jenul Ferdinand 33119805"

class ComputerManager:

    def __init__(self) -> None:
        self.comp_table = LinearProbeTable[str, Computer]()

    def add_computer(self, computer: Computer) -> None:
        """Adds a computer to self.computer_table

        :param computer: The Computer to add 
        :type computer: Computer

        :complexity best & worst: O(1), when no rehashing or probing is required.
        :complexity worst: O(N), where N is the number of items in the table, due to linear probing or when a rehash is triggered.
        """
        self.comp_table[computer.name] = computer

    def remove_computer(self, computer: Computer) -> None:
        """Removes a computer from self.computer_table

        :param computer: The Computer to remove
        :type computer: Computer
        
        :complexity best: O(1), when the computer is found at the initial hash position without probing.
        :complexity worst: O(N), where N is the number of elements in the hash table, occurs when the computer is at the end of a long probe sequence or when rehashing is needed.
        """
        del self.comp_table[computer.name]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """Removes an old computer and adds a new one to self.computer_table

        :param old: The old Computer to remove
        :type old: Computer
        :param new: The new Computer to add
        :type new: Computer

        :complexity best: O(1) when no rehashing or probing is required
        :complexity worst: O(N), where N is the number of items in the table, particularly if rehashing or linear probing is triggered during the operations.
        """
        del self.comp_table[old.name]; self.comp_table[new.name] = new

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """Gives us a list of computers with the specified hacking_difficulty

        :param diff: The specified hacking_difficulty to retrieve Computers
        :type diff: int
        :return: A list of computers with the specified hacking_difficulty
        :rtype: list[Computer]
        
        :complexity best & worst: O(N), each computer must be checked. Where N is the length of the `comp_table`
        """
        return [computer for computer in self.comp_table.values() if computer.hacking_difficulty == diff]

    def group_by_difficulty(self) -> list[list[Computer]]:
        """Groups the computers by their difficulty

        :return: A 2D list which contains the computers grouped by their hacking_difficulty
        :rtype: list[list[Computer]]
        
        :complexity best: O(NlogN), occurs when `self.comp_table` contains computers but they all have the same `hacking_difficulty`. This means that there will only be one group to sort. Where N is the length of the only sublist in `groups` 
        :complexity worst: O(G * NlogN), occurs when all computers in `self.comp_table` have distinct `hacking_difficulty`, leading to as many groups as there are computers. Each group would contain exactly one computer. Where G is the length of the `groups` list. Where N is the length of the each sublist in `groups`
        """
        # Get the maximum difficulty out of all the computers in our table
        max_diff = None
        for comp in self.comp_table.values():
            if max_diff is None or comp.hacking_difficulty > max_diff:
                max_diff = comp.hacking_difficulty
        
        # Get a sublist ready for each difficulty level
        groups = []
        for _ in range(max_diff + 1):
            groups.append([])
        
        # Adding the computers to their hacking_difficulty group
        for comp in self.comp_table.values():
            diff = comp.hacking_difficulty
            groups[diff].append(comp)
        
        # Filter out any empty sublists
        non_empty_groups = []
        for group in groups:
            if group: non_empty_groups.append(group)
        groups = non_empty_groups
        
        # Sort each sub list in groups.
        for i in range(len(groups)):
            groups[i] = mergesort(groups[i])
        
        # Return the grouped computers
        return groups
