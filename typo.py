from typing import List, Tuple

ALPHABET_SIZE = 26

class TrieNode:
    __slots__ = ('children', 'word')
    def __init__(self):
        # Fixed-size array of 26 references (None or TrieNode)
        self.children = [None] * ALPHABET_SIZE
        # Store complete word at terminal nodes
        self.word = None

class Bad_AI:
    def __init__(self, list_words):
        # Create a data structure that stores list_words efficiently for the 
        # next task. 
        # Remember dictionaries (including hashing) & sets are NOT ALLOWED.
        self.root = TrieNode()
        for w in list_words:
            node = self.root
            for ch in w:
                idx = ord(ch) - ord('a')
                if node.children[idx] is None:
                    node.children[idx] = TrieNode()
                node = node.children[idx]
            node.word = w

    def check_word(self, sus_word):
        # This function should identify words with Levenshtein distance
        # value of exactly one (substitution).
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