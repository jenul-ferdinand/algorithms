from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        # Get the position in the hash table for the key
        pos = self.hash(key)
        
        if self.array[pos] is None:
            raise KeyError("Key doesn't exist in hash table")
        
        return self.array[pos][1] # Return the value

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        # If the length of 
        if len(self) == len(self.array) and key not in self:
            raise ValueError("Cannot insert into a full table")
        
        pos = self.hash(key)
        
        if self.array[pos] is None:
            self.count += 1
            
        self.array[pos] = (key, value)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ''
        for item in self.array:
            if item is not None:
                pos = self.hash(item[0])
                
                (key, value) = item
                result += str(pos) + ' (' + str(key) + ', ' + str(value) + ')\n'
        return result
            

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        raise NotImplementedError()

if __name__ == "__main__":
    ht = InfiniteHashTable()
    ht['testing'] = 0
    ht['poo'] = 69
    
    print(ht)