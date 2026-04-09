"""
? Name
Longest Palindrome

? Description
Given a string s which consists of lowercase or uppercase letters, return the
length of the longest palindrome that can be built with those letters.

Letters are case-sensitive, for example, "Aa" is not considered a palindrome.
"""
from collections import defaultdict

def longest_palindrome(string):
    count = defaultdict(int)
    res = 0
    
    for c in s:
        count[c] += 1
        
        if count[c] % 2 == 0:
            res += 2
            
    for cnt in count.values():
        if cnt % 2:
            res += 1
            break
        
    return res
            
    

if __name__ == '__main__':
    # Test 1
    s = "abccccdd"
    res = longest_palindrome(s)
    exp = 7
    assert res == exp, f'Expected {exp}, got {res}'
    
    # Test 2
    s = 'a'
    res = longest_palindrome(s)
    exp = 1
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passsed!')
    
    