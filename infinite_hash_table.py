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
        
        :complexity best & worst: O(N) where N is the no. of locations in the tables.
        """
        locs = self.get_location(key)
        curr = self
        for pos in locs: 
            curr = curr.array[pos][1]
        return curr

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        curr = self
        pos = curr.hash(key)
        
        while curr.array[pos] is not None:
            if not isinstance(curr.array[pos][1], InfiniteHashTable):
                pkey, pvalue = curr.array[pos]
                table = InfiniteHashTable(level=curr.level+1)
                table[pkey] = pvalue
                table[key] = value
                curr.array[pos] = (f'{key[: curr.level + 1]}*', table)
                self.count += 1
                return
            curr = curr.array[pos][1]
            pos = curr.hash(key)
        curr.array[pos] = (key, value)
        self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        locs = self.get_location(key)
        curr = self

        loci = 0
        for loci in range(len(locs)-1):
            curr = curr.array[locs[loci]][1]
        curr.array[locs[len(locs) - 1]] = None
        self.count -= 1
        
        remove = True
        while remove:
            if curr == self:
                break
            
            target = None; num = 0
            for kv in curr.array:
                if kv is not None:
                    if kv[0][len(kv[0]) - 1] != '*':
                        target = kv
                        num = num + 1
            
            if num <= 1 and target:
                target_key, target_value = target
                ptable = self
                for pos in locs[:loci]: ptable = ptable.array[pos][1]
                ptable.array[locs[loci]] = None
                self.count -= 1
                curr = ptable
                loci -= 1
                self[target_key] = target_value
            else:
                remove = False      

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
        :complexity best & worst: O(N), N is the number of tables we need to traverse until we find a key.
        """
        path = [] ; curr = self
        while isinstance(curr, InfiniteHashTable):
            pos = curr.hash(key)
            kv = curr.array[pos]
            if kv is None: raise KeyError(f'Key {key} not found - empty slot encountered.')
            path.append(pos) 
            curr = kv[1] 
        resolved_key, _ = kv
        if resolved_key != key: raise KeyError(f'Key {key}, final resolved key does not match.')
        return path

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

    def sort_keys(self, current : InfiniteHashTable | None = None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        
        :param current: The hash table to start sorting from.
        :type curr: InfiniteHashTable or None
        """
        keys = []
        if current is None: curr = self
        else: curr = current
        
        if curr.array[curr.TABLE_SIZE-1] is not None:
            if '*' not in curr.array[curr.TABLE_SIZE-1][0]:
                keys += [curr.array[curr.TABLE_SIZE - 1][0]]
            
        pos = ord('a') % (self.TABLE_SIZE - 1); tpos = pos
        for _ in range(curr.TABLE_SIZE):
            kv = curr.array[tpos]
            if kv is not None:
                if tpos != curr.TABLE_SIZE-1:
                    key, value = kv
                    if '*' in key: keys += self.sort_keys(value)
                    else: keys += [key]
            tpos = (tpos + 1) % self.TABLE_SIZE
        return keys
                

if __name__ == "__main__":
    ht = InfiniteHashTable()
    ht['testing'] = 0
    ht['poo'] = 69
    
    print(ht)