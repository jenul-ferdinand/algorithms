from typing import List, Tuple


#? =============================================================================|
#? TYPE ALIASES AND CONSTANTS
#? =============================================================================|

# A word is a string of lowercase letters a..z 
Word = str

# Represents a state in the trie traversal
Index = int
Mismatches = int
State = Tuple[Word, Index, Mismatches]

# Fixed alphabet size for lowercase letters
ALPHABET_SIZE = 26


#! =============================================================================|
#! Bad AI Solution
#! =============================================================================|

class TrieNode:
    """
    A class representing a node in a trie.
    
    Alphabet size is fixed to 26 for lowercase letters a..z.
    """
    __slots__ = ('children', 'word', 'mask')
    def __init__(self):
        # Fixed-size array of 26 references (None or TrieNode)
        self.children = [None] * ALPHABET_SIZE
        # Store complete word at leaf nodes
        self.word = None
        # Bitmask of non-null child indicies for fast iteration
        self.mask = 0

class Bad_AI:
    def __init__(
        self, 
        list_words: List[Word]
    ) -> None:
        """
        Function Description:
            Build a prefix trie containing all words from `list_words` to enable
            efficient one-substitution lookups.

        Approach Description:
            For each word, traverse from the root. At each character index:
            
            - If the child node does not exist, create a new TrieNode.
            - Update the current node's mask with the character bit.
            - Move to the child node.
            
            At the end of each word, store it in the node.

        Args:
            list_words: List of unique lowercase words to insert into the trie.

        Time Complexity: O(C)
        Time Complexity Analysis:
            - Each of the C total characters across all words triggers constant
              time operations: computing an index, checking/assigning a child
              pointer.

        Auxiliary Space: O(C)
        Space Complexity Analysis:
            - Up to C new TrieNode instances are created (one per inserted character).
            - Each node allocates a fixed-size `children` list of length 26.

        Notes for Marker:
            Uses a trie with `__slots__` on TrieNode to minimise per-node 
            memory overhead.
        """
        self.root = TrieNode()
        for w in list_words:
            node = self.root
            for ch in w:
                idx = ord(ch) - ord('a')
                if node.children[idx] is None:
                    node.children[idx] = TrieNode()
                node.mask |= (1 << idx)
                node = node.children[idx]
            node.word = w

    def check_word(
        self, 
        sus_word: Word
    ) -> List[Word | None]:
        """
        Function Description:
            Find and return all words in the trie whose substitution-only
            Levenshtein distance to `sus_word` is exactly one.

        Approach Description:
            Use a stack to simulate DFS. Precompute index list of `sus_word`.
            At each state (node, position, mismatches):
            
            1. Follow the matching child (if it exists) without consuming the 
            mismatch.
            2. If no mismatch yet.. Use the node's bitmask to iterate only over
            actual non-matching children for a single substitution.
            
            Collect words at leaf nodes when exactly one mismatch has been used.

        Args:
            sus_word: Target string of lowercase letters to compare.

        Returns:
            A list of words from `list_words` whose substitution-only edit
            distance to `sus_word` is exactly one. Returns an empty list if none.

        Time Complexity: O(J * A + R)
        Time Complexity Analysis:
            - J = length of `sus_word`, A = alphabet size (constant 26).
            - DFS explores at most two recursive paths per depth (match + one
              substitution), scanning A children each time: O(J * A).
            - Appending R result-strings costs O(R) total.

        Auxiliary Space: O(J + R)
        Space Complexity Analysis:
            - Call stack depth: O(J).
            - Result list and collected words: O(R), where R is total length of returned words.
        """
        # Precompute character indicies
        ord_base = ord('a')
        sus_indexes = [ord(c) - ord_base for c in sus_word]
        N = len(sus_indexes)
        
        root = self.root
        result: List[Word] = []
        add_result = result.append

        # Stack holds tuples (node, index in sus_word, mismatches_used)
        stack: List[State] = [(root, 0, 0)]
        while stack:
            node, index, mismatches = stack.pop()
            if index == N:
                if mismatches == 1 and node.word is not None:
                    add_result(node.word)
                continue
            
            orig_idx = sus_indexes[index]
            
            # (1) Exact match branch
            child = node.children[orig_idx]
            if child:
                stack.append((child, index + 1, mismatches))
            
            # (2) Substitution branch (if none used)
            if mismatches == 0:
                # Iterate only over existing children except orig_idx
                subs_mask = node.mask & ~(1 << orig_idx)
                while subs_mask:
                    bit = subs_mask & -subs_mask
                    c = bit.bit_length() - 1
                    next_child = node.children[c]
                    if next_child:
                        stack.append((next_child, index + 1, 1))
                    subs_mask ^= bit
                    
        return result
