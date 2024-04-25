from __future__ import annotations
from algorithms.mergesort import mergesort
from computer import Computer
from data_structures.hash_table import LinearProbeTable

class ComputerManager:

    def __init__(self) -> None:
        self.comp_table = LinearProbeTable[str, Computer]()

    def add_computer(self, computer: Computer) -> None:
        """Adds a computer to self.computer_table

        :param computer: The Computer to add 
        :type computer: Computer

        :complexity best & worst: O(1), __setitem__ is a constant time operation in LinearProbeTable
        """
        self.comp_table[computer.name] = computer

    def remove_computer(self, computer: Computer) -> None:
        """Removes a computer from self.computer_table

        :param computer: The Computer to remove
        :type computer: Computer
        
        :complexity best & worst: O(1), __delitem__ is a constant time operation in LinearProbeTable
        """
        del self.comp_table[computer.name]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """Removes an old computer and adds a new one to self.computer_table

        :param old: The old Computer to remove
        :type old: Computer
        :param new: The new Computer to add
        :type new: Computer

        :complexity best & worst: O(1), __setitem__ and __delitem__ are constant time operations in LinearProbeTable
        """
        del self.comp_table[old.name]; self.comp_table[new.name] = new

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """Gives us a list of computers with the specified hacking_difficulty

        :param diff: The specified hacking_difficulty to retrieve Computers
        :type diff: int
        :return: A list of computers with the specified hacking_difficulty
        :rtype: list[Computer]
        
        :complexity best & worst: O(N), each computer must be checked
        """
        return [computer for computer in self.comp_table.values() if computer.hacking_difficulty == diff]

    def group_by_difficulty(self) -> list[list[Computer]]:
        """Groups the computers by their difficulty

        :return: A 2D list which contains the computers grouped by their hacking_difficulty
        :rtype: list[list[Computer]]
        
        :complexity best: O(1) occurs when we only have one computer in self.computer_table
        :complexity worst: O(N * new_mergesort) 
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
        
        # Sort each sub list of the within the grouped computers.
        for i in range(len(groups)):
            groups[i] = mergesort(groups[i])
        
        # Return the grouped computers
        return groups