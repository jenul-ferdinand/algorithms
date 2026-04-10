# Question

Case 2b of the Z-algorithm (i.e., the case handling the scenario where k ≤ r and Z[k − l + 1] ≥ r − k + 1) can be further decomposed into two distinct
cases:

- case 2b.1 Z[k − l + 1]> r − k + 1
- case 2b.2 Z[k − l + 1]= r − k + 1

Justify that when Z[k − l + 1] > r − k + 1, then one can immediately conclude
that Z[k] = r − k + 1 without needing any explicit character comparisons. In
other words, explicit character comparisons are only needed for
the Z[k − l + 1] = r − k + 1 case.

# Answer

Z[k-l+1] is the previously computed value mirrored at the prefix corresponding
to k.

In the case where Z[k-l+1] > r-k+1 we know that the mirror extends past the
Z-box. Hence the values have already been pre-computed.

But we know that we can't go past r because it's the limit given by the z-box.
In a previous situation we've already concluded that there is no match past this
stage.

Therefore we can conclude that Z[k] = r-k+1 with no more character comparisons.
