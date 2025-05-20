from typing import List, Tuple

# A word is a string of lowercase letters a..z 
Word = str

# Fixed alphabet size for lowercase letters
ALPHABET_SIZE = 26

class TrieNode:
    """
    A class representing a node in a trie.
    
    Alphabet size is fixed to 26 for lowercase letters a..z.
    """
    __slots__ = ('children', 'word')
    def __init__(self):
        # Fixed-size array of 26 references (None or TrieNode)
        self.children = [None] * ALPHABET_SIZE
        # Store complete word at     terminal nodes
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
        
        def dfs(node: TrieNode, i, mismatches):
            # If we've processed all characters
            if i == n:
                # Exactly one substitution and end of word
                if mismatches == 1 and node.word is not None:
                    result.append(node.word)
                return
            
            orig_idx = ord(sus_word[i]) - ord('a')
            # Try matching and substitution
            for c in range(ALPHABET_SIZE):
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
    expected_outputs = [
        ['aba'],        # For 'aaa': 'aba' (a->b is 1 sub)
        ['aaa', 'aba'], # For 'axa': 'aaa' (x->a), 'aba' (x->b)
        [],             # For 'ab': No word of length 2 is 1 sub away. Words must be same length.
        [],             # For 'xxx': 'xyz' is 1 sub (x->z). Oh, my example trace was faulty.
                        # 'xyz' vs 'xxx': x==x, y!=x (sub), z!=x (sub). Dist 2.
                        # The example output for 'xxx' is []. This is correct.
                        # 'xyz' is 1 sub from 'xxz', 'xyx', 'ayz', etc. Not 'xxx' unless len is also 1.
        ['aaaa']        # For 'aaab': 'aaaa' (b->a is 1 sub)
    ]
    my_ai = Bad_AI(list_words)
    all_tests_passed = True
    for i, sus_word in enumerate(list_sus):
        my_answer = my_ai.check_word(sus_word)
        # Sort for consistent comparison, as order in result list might vary
        # though the DFS structure might lead to a specific order.
        my_answer.sort() 
        expected_output = expected_outputs[i]
        expected_output.sort()

        if my_answer == expected_output:
            print(f"Test for '{sus_word}': Passed. Got {my_answer}")
        else:
            print(f"Test for '{sus_word}': Failed. Expected {expected_output}, Got {my_answer}")
            all_tests_passed = False

    if all_tests_passed:
        print("\nAll provided examples passed.")
    else:
        print("\nSome examples failed.")

    # Additional test cases
    print("\nAdditional Tests:")
    list_words_2 = ["apple", "apply", "axply", "apricot", "banana"]
    ai_2 = Bad_AI(list_words_2)

    sus_word_2 = "axple" # Expect ["apple"] (x->p)
    expected_2 = ["apple", "axply"]
    res_2 = ai_2.check_word(sus_word_2)
    res_2.sort()
    assert res_2 == expected_2, f"Test for '{sus_word_2}': Expected {expected_2}, Got {res_2}"
    print(f"Test for '{sus_word_2}': Passed. Got {res_2}")

    sus_word_3 = "apxly" # Expect ["apply"]
    expected_3 = ["apply"]
    res_3 = ai_2.check_word(sus_word_3)
    res_3.sort()
    expected_3.sort()
    assert res_3 == expected_3, f"Test for '{sus_word_3}': Expected {expected_3}, Got {res_3}"
    print(f"Test for '{sus_word_3}': Passed. Got {res_3}")

    sus_word_4 = "apricots" # Length mismatch, expect []
    expected_4 = []
    res_4 = ai_2.check_word(sus_word_4)
    assert res_4 == expected_4, f"Test for '{sus_word_4}': Expected {expected_4}, Got {res_4}"
    print(f"Test for '{sus_word_4}': Passed. Got {res_4}")

    sus_word_5 = "axxyz" # No match
    expected_5 = []
    res_5 = ai_2.check_word(sus_word_5)
    assert res_5 == expected_5, f"Test for '{sus_word_5}': Expected {expected_5}, Got {res_5}"
    print(f"Test for '{sus_word_5}': Passed. Got {res_5}")

    list_words_3 = ["cat", "bat", "cot", "cog", "dog"]
    ai_3 = Bad_AI(list_words_3)
    # Test 5 (Corrected expectation)
    sus_word_3_1 = "cot"
    expected_3_1 = ["cat", "cog"] # "bat" is 2 subs, "dog" is 2 subs from "cot"
    expected_3_1.sort()
    res_3_1 = ai_3.check_word(sus_word_3_1)
    res_3_1.sort()
    if res_3_1 == expected_3_1:
        print(f"Test for '{sus_word_3_1}': Passed. Got {res_3_1}")
    else:
        print(f"Test for '{sus_word_3_1}': Failed. Expected {expected_3_1}, Got {res_3_1}")