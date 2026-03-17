For a string S[1..n]
Where Z[2] = Len > 0.
The values of Z[k] for 3 <= k <= Len+2
Can be resolved without comparisons when all characters are the same,
This reuses previous r-k+1 values because case 2b kicks in for every Z[k] value after the base case.