from typing import List, Tuple

# A word is a string of lowercase letters a..z 
Word = str

# Fixed alphabet size for lowercase letters
ALPHABET_SIZE = 26

class TrieNode:
    __slots__ = ('children', 'word')
    def __init__(self):
        # Fixed-size array of 26 references (None or TrieNode)
        self.children = [None] * ALPHABET_SIZE
        # Store complete word at terminal nodes
        self.word = None

class Bad_AI:
    def __init__(
        self, 
        list_words: List[Word]
    ) -> None:
        """
        Builds a trie storing list_words for subsequent 1-substitution searches.
        
        Time Complexity: O(C)
        Space Complexity: O(C)
        Where:
        - C is the total number of characters in list_words.
        """
        self.root = TrieNode()
        for w in list_words:
            node = self.root
            for ch in w:
                idx = ord(ch) - ord('a')
                if node.children[idx] is None:
                    node.children[idx] = TrieNode()
                node = node.children[idx]
            node.word = w

    def check_word(
        self, 
        sus_word: Word
    ) -> List[Word]:
        """
        Return all words from list_words whose Levenshtein distance to sus_word
        is exactly one (allowing only substitution).
        
        Time Complexity: O(J * N) + O(X)
        Auxiliary Space Complexity: O(X)
        Where:
        - J is the length of sus_word
        - N is the length of list_words
        - X is the total number of characters returned.        
        """
        result = []
        n = len(sus_word)
        
        def dfs(node, i, mismatches):
            # If we've processed all characters
            if i == n:
                # Exactly one substitution and end of word
                if mismatches == 1 and node.word is not None:
                    result.append(node.word)
                return
            
            orig_idx = ord(sus_word[i]) - ord('a')
            # Try matching and substitution
            for c in range(26):
                child = node.children[c]
                if not child:
                    continue

                # Matching character
                if c == orig_idx:
                    dfs(child, i + 1, mismatches)
                    
                # Substitution (if none yet)
                elif mismatches == 0:
                    dfs(child, i + 1, 1)
                    
        dfs(self.root, 0, 0)
        return result
    
if __name__ == '__main__':
    # Example from spec
    list_words = ['aaa', 'abc', 'xyz', 'aba', 'aaaa']
    list_sus = ['aaa', 'axa', 'ab', 'xxx', 'aaab']
    expected = [
        ['aba'],
        ['aaa', 'aba'],
        [],
        [],
        ['aaaa']
    ]
    my_ai = Bad_AI(list_words)
    for sus_word, exp in zip(list_sus, expected):
        result = my_ai.check_word(sus_word)
        assert result == exp, f"For {sus_word!r}, expected {exp}, got {result}"
    print("All tests passed.")