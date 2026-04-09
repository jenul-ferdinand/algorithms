class SuffixArrayNaive:
    """
    Naive construction of suffix array
    
    Creates a suffix array `sa` for a given string `S`.
    
    Time Complexity: O(n^2 log n)
    Time Complexity Analysis:
        - Sorting the suffixes, comparing costs O(n) hence O(n^2)
        
    Auxiliary Space Complexity: O(n)
    Auxiliary Space Complexity Analysis:
        - Storing suffixes array for n suffix-index pairs = O(n^2)

    Terms: 
    - n: The length of the string S
    """
    def __init__(self, S: str):
        self.S = S
        n = len(S)
        
        suffixes = [(S[i:], i) for i in range(n)]
        suffixes.sort(key = lambda pair: pair[0])
        self.sa = [idx for (_, idx) in suffixes]
        
class SuffixArray:
    """
    Prefix doubling technique for constructing suffix array.
    
    Time Complexity:
    
    
    """
    pass

if __name__ == '__main__':
    # Example 1: “banana$”
    #   Suffixes:
    #     0: "banana$"
    #     1: "anana$"
    #     2: "nana$"
    #     3: "ana$"
    #     4: "na$"
    #     5: "a$"
    #     6: "$"
    #
    # In lex order: "$"(6), "a$"(5), "ana$"(3), "anana$"(1), "banana$"(0), "na$"(4), "nana$"(2)
    s1 = "banana$"
    sa1 = SuffixArrayNaive(s1)
    expected1 = [6, 5, 3, 1, 0, 4, 2]
    assert sa1.sa == expected1, f"banana$ → expected {expected1}, got {sa1.sa}"
    
    # Example 2: “abracadabra$”
    # We can verify by sorting (suffix, index) pairs with Python’s built-in sorting:
    s2 = "abracadabra$"
    sa2 = SuffixArrayNaive(s2)
    expected2 = [idx for (_, idx) in sorted((s2[i:], i) for i in range(len(s2)))]
    assert sa2.sa == expected2, f"abracadabra$ → expected {expected2}, got {sa2.sa}"
    
    print('All tests passed!')