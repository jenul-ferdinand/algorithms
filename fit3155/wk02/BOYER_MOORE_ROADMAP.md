- [x] Naive pattern matching baseline
    - Try every alignment and scan left to right.
    - Goal: see the repeated work Boyer-Moore avoids.

- [x] Right-to-left scanning
    - Still test one alignment at a time, but compare from the end of the pattern.
    - Goal: when a mismatch happens, the already-matched part is a suffix of the pattern.

- [x] Basic bad character rule
    - Implemented in `boyermoore_basic.py`.
    - Store `R(x)`, the rightmost occurrence of each character in the pattern.
    - On mismatch at pattern index `k` with bad character `x`, shift by `max(k - R(x), 1)`.
    - Goal: use the mismatching text character as evidence.

- [x] Extended bad character rule
    - Implemented in `boyermoore_extendedbcr.py`.
    - Store `R_k(x)`, the rightmost occurrence of `x` before position `k`.
    - On mismatch, shift by `k - R_k(x)`.
    - Goal: avoid the weak case where basic BCR sees an occurrence to the right of the mismatch.

- [x] Z-suffix preprocessing
    - Implemented in `process_z_suffix()` inside `boyermoore_gs.py`.
    - Compute Z on the reversed pattern, then reverse the result.
    - Goal: know which substrings ending inside the pattern also match a suffix of the pattern.

- [x] Good suffix rule
    - Implemented in `process_gs()` and `boyermoore_goodsuffix.py`.
    - If `pat[k + 1..m - 1]` matched before the mismatch, align it with its rightmost earlier occurrence.
    - Goal: use the matched suffix as evidence.

- [x] Matched prefix rule
    - Implemented in `process_mp()` and `boyermoore_mp.py`.
    - If the good suffix has no useful earlier occurrence, align its longest suffix that is also a prefix of the pattern.
    - Also handles the shift after a full match.
    - Goal: give the good suffix rule a safe fallback.

- [x] Combine shift evidence
    - Use the extended bad character shift and the good suffix / matched prefix shift.
    - Shift by the larger safe value.
    - Goal: choose the strongest valid reason to move the pattern.

- [x] Galil's optimisation
    - Implemented in `boyermoore_optimised.py`.
    - After a good suffix or matched prefix shift, remember the region that is already known to match.
    - Skip that region during the next right-to-left scan.
    - Goal: avoid rechecking characters that the previous shift already proved.

- [x] Big picture
    - Boyer-Moore is not one trick.
    - It is right-to-left scanning plus safe shifts from two pieces of evidence:
        - the bad character,
        - the good suffix.
    - Matched prefix handles the fallback case.
    - Galil's optimisation stops the algorithm from paying again for characters it already knows.
