""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Jackson Goerner'
__since__ = '07/02/2023'


from typing import TypeVar, Generic
from data_structures.referential_array import ArrayR

K = TypeVar('K')
V = TypeVar('V')

class FullError(Exception):
    pass


class LinearProbeTable(Generic[K, V]):
    """
    Linear Probe Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array:ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _linear_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing.
        :complexity best: O(hash(key)) first position is empty
        :complexity worst: O(hash(key) + N*comp(K)) when we've searched the entire table
                        where N is the tablesize
        :raises KeyError: When the key is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        # Initial position
        position = self.hash(key)

        for _ in range(self.table_size):
            if self.array[position] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    return position
                else:
                    raise KeyError(key)
            elif self.array[position][0] == key:
                return position
            else:
                # Taken by something else. Time to linear probe.
                position = (position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key)

    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

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

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :complexity: See linear probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key, False)
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See linear probe.
        :raises FullError: when the table cannot be resized further.
        """

        position = self._linear_probe(key, True)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :complexity best: O(hash(key)) deleting item is not probed and in correct spot.
        :complexity worst: O(N*hash(key)+N^2*comp(K)) deleting item is midway through large chain.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key, False)
        # Remove the element
        self.array[position] = None
        self.count -= 1
        # Start moving over the cluster
        position = (position + 1) % self.table_size
        while self.array[position] is not None:
            key2, value = self.array[position]
            self.array[position] = None
            # Reinsert.
            newpos = self._linear_probe(key2, True)
            self.array[newpos] = (key2, value)
            position = (position + 1) % self.table_size

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # Cannot be resized further.
            return
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                key, value = item
                self[key] = value

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N * (str(key) + str(value))) where N is the table size
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
