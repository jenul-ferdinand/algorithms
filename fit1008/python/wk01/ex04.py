"""
We will now write a program to calculate the digital root of a number.

The digital root of a decimal integer is obtained by adding up its digits and
then repeating this process to the result, and so on until you get a single
digit. The single-digit is the digital root of the decimal integer you started
with.

As an example: to find the digital root of 979853562951413, we calculate: sum of
digits = 9 + 7 + 9 + 8 + 5 + 3 + 5 + 6 + 2 + 9 + 5 + 1 + 4 + 1 + 3 = 77, then
sum of digits = 7 + 7 = 14, then sum of digits = 1 + 4 = 5. Now we have just
one digit, 5, so that's the digital root of the number we started with.

Write a program that calculates the digital root of an integer. Must run in O(n)
"""


def digital_root_best_way(n: int):
    return 1 + (n - 1) % 9


def digital_root(n):
    n = [int(digit) for digit in str(n)]

    while len(n) > 1:
        n = [int(digit) for digit in n]
        n = list(str(sum(n)))

    return int(n[0])
