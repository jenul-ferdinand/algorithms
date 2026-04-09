Problem 2 answer:

For a string S[1..n]
Where Z[2] = Len > 0.
The values of Z[k] for 3 <= k <= Len+2
Can be resolved without comparisons when all characters are the same,
This reuses previous r-k+1 values because case 2b kicks in for every Z[k] value after the base case.

Problem 3 answer:

For this, since all characters are the same, the case that will kick in for the 
remaining characters when k > 2, is case 2b because the current substring will
always be larger than the current zbox's right position.

