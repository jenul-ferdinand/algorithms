from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

__author__ = "Jenul Ferdinand 33119805"

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _init_inner_table(self) -> LinearProbeTable:
        """
        Creates an internal hash table.
        
        :complexity best & worst: O(N), occurs when we initialise LinearProbeTable with an array with size TABLE_SIZES[size_index], where N is the size of the table of LinearProbeTable.
        """
        table = LinearProbeTable(self.internal_sizes)
        table.hash = lambda k: self.hash2(k, table)
        return table

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        :complexity best: O(hash(key1) + N * _linear_probe), occurs when self.array[outer_pos] is not None, where N is the table size.
        :complexity worst: O(hash(key1) + N * (_linear_probe + _init_inner_table)), occurs when self.array[outer_pos] is None, where N is the table size.
        """
        outer_pos = self.hash1(key1)
        step_size = 1
        for _ in range(self.table_size): 
            if self.array[outer_pos] is None:
                if is_insert:
                    internal_table = self._init_inner_table()
                    self.array[outer_pos] = (key1, internal_table)
                    
                    if key2 is not None:
                        inner_pos = internal_table._linear_probe(key2, True)
                        return (outer_pos, inner_pos)
                    return outer_pos
                else:
                    raise KeyError(f'Key not found: {key2}')
            elif self.array[outer_pos][0] == key1:
                if key2 is not None:
                    internal_table = self.array[outer_pos][1]
                    inner_pos = internal_table._linear_probe(key2, is_insert)
                    return outer_pos, inner_pos
                return outer_pos
            else:
                outer_pos = (outer_pos + step_size) % self.table_size
        
        raise FullError('Table is full noob')
        
    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
            
        :complexity best: O(1), when yielding the first available key
        :complexity worst: O(N), for a full traversal for keys, where N is the size of either the inner or outer tables.
        """
        if key is None:
            for entry in self.array:
                if entry is not None:
                    yield entry[0]
        else:
            outer_pos = self._linear_probe(key, None, False)
            inner_table = self.array[outer_pos][1]
            for entry in inner_table.array:
                if entry is not None:
                    yield entry[0]

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
            
        :complexity best: O(1), when yielding the first available value
        :complexity worst: O(N), for a full traversal for values, where N is the size of either the inner or outer tables.
        """
        if key is None:
            for entry in self.array:
                if entry is not None:
                    inner_table = entry[1]
                    for value in inner_table.array:
                        if value is not None:
                            yield value[1] 
        else:
            pos_top = self._linear_probe(key, None, False)
            inner_table = self.array[pos_top][1]
            for value in inner_table.array:
                if value is not None:
                    yield value[1]

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        
        :complexity best: O(1), occurs when iter_keys yields the first available key.
        :complexity worst: O(N), occurs when iter_keys must do a full traversal of keys, where N is the size of either the inner or outer tables.
        """
        _list = []
        
        if key is None:
            for key in self.iter_keys(): _list.append(key)
        else:
            for key in self.iter_keys(key): _list.append(key)
                
        return _list

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :complexity best: O(1), occurs when iter_values yields the first available value.
        :complexity worst: O(N), occurs when iter_valies must do a full traversal of values, where N is the size of either the inner or outer tables.
        """
        _list = []
        
        if key is None: 
            for value in self.iter_values(): _list.append(value)
        else: 
            for value in self.iter_values(key): _list.append(value)
            
        return _list

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        
        :complexity best & worst: O(_linear_probe)
        """

        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        
        :complexity best & worst: O(_linear_probe) 
        """

        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        :complexity best: O(len(key)), occurs when the item is found at the first position.
        :complexity worst: O(len(key) + N * _linear_probe), occurs when we must do a full traversal, where N is the size of the table.
        """
        key1, key2 = key
        outer_pos, inner_pos = self._linear_probe(key1, key2, False)
        internal_table = self.array[outer_pos][1]
        del internal_table[key2]
        self.count -= 1
        
        if internal_table.is_empty():
            self.array[outer_pos] = None
        
        outer_pos = (outer_pos + 1) % self.table_size
        while self.array[outer_pos] is not None:
            key1, internal_table = self.array[outer_pos]
            self.array[outer_pos] = None
            new_outer_pos = self._linear_probe(key1, None, True)
            self.array[new_outer_pos] = (key1, internal_table)
            outer_pos = (outer_pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N * hash(K)) No probing.
        :complexity worst: O(N * hash(K) + N^2 * comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            return None
        self.array = ArrayR[tuple[K1, LinearProbeTable[K2, V] | None]](self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                key1, old_inner_table = item
                new_inner_table = self._init_inner_table()
                for inner_item in old_inner_table.array:
                    if inner_item is not None:
                        key2, value = inner_item
                        new_inner_table.__setitem__(key2, value)
                        
                self.array[self._linear_probe(key1, None, True)] = (key1, new_inner_table)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = []
        for index1 in range(len(self.array)):
            entry = self.array[index1]
            if entry is not None:
                key1, sub_table = entry
                sub_entries = []
                for index2 in range(len(sub_table.array)):
                    sub_entry = sub_table.array[index2]
                    if sub_entry is not None:
                        key2, value = sub_entry
                        sub_entries.append(f"{key2}: {value}")
                if sub_entries:
                    result.append(str(key1) + " -> {{ " + ", ".join(sub_entries) + " }}")
        return "\n".join(result)
    
if __name__ == "__main__":
    # Create an instance of DoubleKeyTable
    dkt = DoubleKeyTable[str, str, int]()

    # Test inserting items
    dkt['Tim', 'Jen'] = 1
    dkt['Tim', 'James'] = 2
    dkt['Tim', 'John'] = 4
    dkt['John', 'Foo'] = 432432
    dkt['John', 'Doo'] = 31312312312
    
    print(dkt.values()) # Should return [1, 4, 2, 31312312312, 432432]
    
    # Testing iter_keys()
    print('=== TESTING iter_keys() ===')
    for key2 in dkt.iter_keys('Tim'):
        print(f'Tim, {key2}')
    for key2 in dkt.iter_keys('John'):
        print(f'John, {key2}')
        
    # Testing iter_values()
    dkt['Jen', 'Test'] = 3131312231 
    dkt['Jen', 'Poopie'] = 321312312435234523 
    dkt['Jen', 'Dude'] = 699696969696969696996 
    for j in dkt.iter_values('Jen'):
        print(j)

    # Display the stored values
    print("Initial Entries:")
    print(dkt)
