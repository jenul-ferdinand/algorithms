# Question

Prove that the Z-algorithm runs in O(N) time requiring O(N) space in the worst case, where N is the length of the input string.

# Answer

The z algorithm takes a string of size N, creates and stores a z array of size N. So the space complexity is O(N).

It iterates through each value in the string; updating the z array in each
iteration. This means that the time complexity in the worst case is O(N).
