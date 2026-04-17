"""
We read the character then loop until we reac a different character,
counting how many we met
"""


def rlencode(string: str) -> str:
    """
    Run-Length-Encoding

    Encodes a string to be smaller by numerating repeating values.
    E.g., aaaabbbb -> a4b4

    Time complexity: O(n)
    Space complexity: O(n)
    """
    n = len(string)
    count = 0
    curr = string[0]
    output = ""

    for i in range(n):
        if string[i] == curr:
            count += 1
        else:
            output += f"{curr}{count}"
            curr = string[i]
            count = 1

            # edge-case when a singular value is left in the end
            if i == n - 1:
                output += f"{curr}{count}"

    return output


def rldecode(string: str) -> str:
    """
    Run-Length-Decode

    Just reversed it back to the original string.
    """

    import re

    numbers = re.split(r"[a-zA-Z]", string)
    numbers.pop(0)  # remove first empty val
    numbers = [int(x) for x in numbers]

    letters = re.split(r"[0-9]", string)
    letters = [x for x in filter(None, letters)]  # clean empty vals

    output = ""
    for count, char in zip(numbers, letters):
        count = int(count)
        output += f"{char * count}"

    return output


if __name__ == "__main__":
    string = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB"
    result = rlencode(string)
    output = "W12B1W12B3W24B1"
    assert result == output, f"Exp: {output}, Got: {result}"

    encoded = "W12B1W12B3W24B1"
    result = rldecode(encoded)
    decoded = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB"
    assert result == decoded, f"Exp: {decoded}, Got: {result}"
