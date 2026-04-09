from typing import List, Tuple

Word = str | None
Boolean = bool

class TrieNode:
    """
    A class representing a node in a Prefix Trie
    
    Alphabet size of 26 for lowercase letters a-z.
    """
    __slots__ = ('children', 'word')
    def __init__(self, alphabet_size: int = 26):
        self.children = [None] * alphabet_size
        
        self.word: Word = None
        
class Trie:
    """
    A class representing a Prefix Trie
    
    """
    def __init__(self, list_words: List[Word]):
        # Create the root empty node for the trie
        self.root = TrieNode()
        
        # Go through each word in the list and add to the trie
        for word in list_words:
            # Declare the root node 
            node = self.root
            
            # For each character we create a child node
            for char in word:
                index = ord(char) - ord('a')
                
                if node.children[index] is None:
                    node.children[index] = TrieNode()
                    
                node: TrieNode = node.children[index]
                
            node.word = word
            
    def starts_with(self, prefix: str) -> bool:
        pass # TODO: Implement this
    
    def search(self, word: str) -> bool:
        pass # TODO: Implement this
    
    def insert(self, word: str) -> bool:
        pass # TODO: Implement this
    
if __name__ == '__main__':
    pass
            
        
                
        