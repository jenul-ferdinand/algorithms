"""
Write a python function that asks for an input from the user and tells if that
number is higher or lower than a target number provided. User the scaffold
provided.

Must be O(1)
"""


def higher_lower(num, target):
    return "higher" if num < target else "lower" if num > target else "correct"
