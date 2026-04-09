I optimised zalg by removing the explicit checks between case 2a and 2b. 
I did this by using the `min` function, allowing me to take which ever is smaller between the remaining distance from k to the right end of the z box (`right - k`) or either the z value of the mirrored position of k in the prefix (`z[k - left]`).

We take the smaller one because it's the limit of what we can confidently claim without explicit comparisons.

The larger value's extra information can fall outside our zbox right end.
Which allows us to simply switch between just setting z[k] = z[k - left] (case 2a, reuse) or just setting it to the remaining distance as z[k] = right - k which starts case 2b.