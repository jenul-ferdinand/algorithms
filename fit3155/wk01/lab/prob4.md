Z[k-l+1] is the mirror image at the prefix of Z[k].

In the case where Z[k-l+1] > r-k+1 we know that the mirror extends past the Z-box. Hence the values have already been pre-computed.
So we can just set Z[k] = r-k+1 because that's the count of characters that remain from k to r inclusive.
This will be the minimum value of Z[k]. 
Note that the case Z[k-l+1] = r-k+1 can also kick in, meaning that this minimum value of Z[k] we set; can be increased there further if more manual comparisons are made past r; stopping at the first mismatch.