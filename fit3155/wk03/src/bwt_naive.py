def bwt_naive(string):
    """
    Naively algorithms for the BWT of a given string.

    Let r be the length of the rotations array
    Let n be the length of the input string

    1. Finds all cyclical rotations
        - O(n) time, O(n) space

    2. Sorts those rotations lexicographically
        - O(n^2 log n) time, O(1) space
        - It's n^2 because we're not just comparing characters, we're comparing
          two strings lexicographically. Otherwise it would be n log n.

    3. Create a r x n matrix, appending the rotations in order.
        - O(rn) = O(n^2) time to construct because r is >= n
        - O(n^2) space

    3. Take the last column of the matrix for BWT string

    Time complexity: O(n^2 log n)
    Space complexity: O(n^2)
    """
    if string[-1] != "$":
        string = string + "$"

    N = len(string)

    # Create the array of all cyclical rotations
    rotations = []
    for i in range(0, N):
        j = 0
        substr = ""
        while j + i < N + i:
            substr += (string + string)[i + j]
            j += 1

        rotations.append(substr)

    # Sort the rotations lexicographically
    # Appending those into the BWT matrix in order
    # The matrix will have R rows and N columns.
    rotations.sort()
    R = len(rotations)
    MATRIX = [[char for char in rotations[i]] for i in range(R)]
    print(MATRIX)

    # Take the last character from the BWT matrix
    BWT = ""
    for row in MATRIX:
        BWT += row[-1]

    print(BWT)
    return BWT


bwt_naive("googol")
