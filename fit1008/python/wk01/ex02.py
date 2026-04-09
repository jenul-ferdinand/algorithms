"""
Extend your previous program that accepts n inputs from a user until the user
is able to guess the right answer.

Must be O(n), where n is the number of inputs
"""


def higher_lower(target):
    guessed = False
    while not guessed:
        num = int(input("Enter a number: "))
        print("lower" if num > target else "higher")
        if num == target:
            print("correct")
            break
