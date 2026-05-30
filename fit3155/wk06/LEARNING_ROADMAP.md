# Week 6: Semi-numerical algorithms - Learning Roadmap

Source material: `notes06.pdf`, `seminar06.pdf`, `lab06.pdf`, `fermat-little-theorem.pdf`.
Lab exercises drawn from `lab06.pdf` are woven in as checkpoints under each topic.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab06.pdf`. `[ ] Lab notes-Qx`: question embedded in `notes06.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

---

## 1. Karatsuba multiplication

- [x] Positional notation in arbitrary base
    - U = (u_1 u_2 ... u_d)_b interpreted as sum of u_i * b^(d-i).
    - Goal: write the closed-form formula for any base b.
    - [X] Lab Q1: write the integer formula for U in base b.
    - [X] Lab Q2: identify the base Python's Bignum uses internally (it is not 2).
- [X] Why long multiplication is O(n*m)
    - Goal: argue the bound for n-digit by m-digit long multiplication.
- [X] Decomposition trick
    - u = 2^d * U_1 + U_0, v = 2^d * V_1 + V_0.
    - FOIL gives 4 sub-products, the middle two are needed only as a sum.
    - Goal: derive uv = (2^(2d) + 2^d) U_1 V_1 - 2^d (U_1 - U_0)(V_1 - V_0) + (2^d + 1) U_0 V_0 from scratch.
- [X] Why 3 sub-multiplications instead of 4
    - (U_1 - U_0)(V_1 - V_0) = U_1 V_1 - U_1 V_0 - U_0 V_1 + U_0 V_0 recovers the cross term using products you already need.
    - Goal: explain the saving without looking at notes.
- [X] Recursion
    - Each sub-product is half the size, recurse until 1-bit base case.
    - Goal: draw the recursion tree and count leaves.
- [X] Recurrence and complexity
    - T(2d) = 3 T(d) + cd.
    - Goal: solve to O(d^log_2(3)) ~ O(d^1.585).
    - [X] Lab Q4: solve T(2d) = 3T(d) + cd by hand without the Master Theorem.
- [X] Generalisation to arbitrary base
    - Goal: redo the decomposition with base b instead of 2; reason about the ideal base when the machine word size is w.
    - [X] Lab Q3: generalise Karatsuba to base b and reason about the best base for word size w.
- [X] Implementation
    - File: `src/karatsuba.py`.
    - Goal: reproduce from memory, including the 1-bit base case.
    - [X] Lab Impl 3: divide-and-conquer multiplication of two integers.

---

## 2. Modular arithmetic foundations

- [x] Theorem 1: division
    - For integer a and positive integer n, unique q, r exist with a = qn + r and 0 <= r < n.
    - Goal: state the theorem and identify quotient and remainder.
- [x] Definition: congruence classes
    - a is congruent to b mod n iff a - b is an integer multiple of n.
    - Goal: explain why dividing Z by n produces exactly n classes.
- [x] The product-mod property
    - xy mod z = ([x mod z] * [y mod z]) mod z.
    - Goal: prove it (start by interpreting the LHS using the congruence-class definition).
    - [x] Lab notes-Q3: prove the property.
- [x] Why this property matters
    - Goal: explain in one sentence why it is the key to avoiding the giant numbers in naive modular exponentiation.

---

## 3. Modular exponentiation by repeated squaring

- [x] Naive approach and why it explodes
    - Compute a^b by b-1 multiplications, then mod n at the end.
    - Time is O(2^(2 d_b) d_a^2 + 2^(d_b) d_a d_n), exponential in d_b.
    - Goal: explain why the bottleneck is the size of the intermediate a^b, not the number of multiplications.
- [x] Binary decomposition of the exponent
    - b = sum of 2^i for bits set in b. So a^b = product of a^(2^i) for those i.
    - Goal: rewrite a^560 as a product of squarings (worked example in notes).
- [x] Repeated squaring
    - x_i = (x_(i-1))^2 mod n. Multiply into result whenever bit i of b is 1.
    - Goal: walk the LSB-to-MSB pseudocode (notes pg 11) for a small example.
    - [x] Lab Q5: can MSB-to-LSB also recover the integer from a binary representation? Explain.
    - [x] Lab Q6: can modular exponentiation be done MSB-to-LSB? If yes, write its pseudocode.
    - [x] Lab Q7: compute 7^330 mod 13 by hand using repeated squaring.
- [ ] Complexity (NOT EXAMINABLE but worth deriving once)
  - O(d_a d_n + d_b d_n^2). Compare against the naive bound.
  - Goal: identify which term comes from squaring vs. modulo division vs. result updates.
- [x] Implementation
  - File target: `src/modular_exponentiation.py`.
  - Goal: implement and test against Python's built-in `pow(a, b, n)`.
  - [x] Lab Impl 1: implement modular exponentiation by repeated squaring.

---

## 4. Naive primality testing

- [x] Definition of prime
    - Goal: state cleanly and recall there are 25 primes below 100.
- [x] Trial division
    - Try every k in [2, n-1]; if any divides n, composite.
    - Goal: write the pseudocode from memory.
- [x] Complexity: O(n d_n^2) = O(2^(d_n) d_n^2)
    - Improving to k <= sqrt(n) gives O(2^(d_n / 2) d_n^2). Still exponential in d_n.
    - Goal: explain why trial division is unusable for 1024-bit RSA primes.
- [ ] RSA motivation
    - n = p q, public/private key pair, security rests on the hardness of factoring n.
    - Goal: state in one sentence why fast probabilistic primality testing is necessary.

---

## 5. Fermat's little theorem and the Fermat randomised test

- [x] Theorem 2: Fermat's little theorem
    - If p is prime, a^p is congruent to a mod p. Equivalently a^(p-1) is ;congruent to 1 mod p when gcd(a, p) = 1.
    - Goal: state both forms.
- [ ] Proof of Fermat's little theorem (NOT EXAMINABLE, but read it)
    - Argued via the p-1 nonzero multiples of a mod p forming a permutation of {1, ..., p-1}.
    - Source: notes06.pdf pp 14-15, plus `fermat-little-theorem.pdf`.
    - Goal: follow the chain a*2a*...*(p-1)a == (p-1)! a^(p-1), conclude a^(p-1) == 1 mod p.
- [x] Fermat randomised test
    - Pick random a in (1, n-1), check a^(n-1) mod n == 1. If not, composite.
    - Goal: write the pseudocode and explain why the witness range excludes 1 and n-1.
    - [ ] Lab Q8 (= Question 4 in notes): show that for a = 1 and a = n - 1 the congruence holds trivially for any odd n.
- [x] Pseudoprimes and Fermat liars
    - A composite n that satisfies the test for some base a is a pseudoprime to base a; a is a Fermat liar.
    - Goal: explain why the test can return a false positive but never a false negative.
- [x] Carmichael numbers
    - Composites that are pseudoprime to every base coprime to them; 561 is the smallest.
    - Goal: describe what goes wrong with the Fermat test on a Carmichael number.
- [x] Implementation
    - File target: `src/fermat_test.py`.
    - Goal: implement and observe it being fooled by 561 with witness a = 7, then catching it with a = 3.

---

## 6. Square roots of unity (mod p)

- [ ] Theorem 3: square roots of unity
    - If p is an odd prime, the only solutions to x^2 == 1 mod p are x == +1 or x == -1 mod p.
    - Goal: state precisely.
    - [ ] Lab Q10a: determine all solutions to y^2 == 1 mod n when n is prime.
    - [ ] Lab Q10b: argue whether more solutions can exist when n is composite, and justify.
- [ ] Why this is the bridge to Miller-Rabin
    - If a sequence of repeated squarings ever produces 1 from something that is not +1 or -1 mod n, then n cannot be prime.
    - Goal: explain in one sentence why this gives a way to detect Carmichael numbers that Fermat misses.

---

## 7. Miller-Rabin primality test

- [ ] Decompose n - 1 = 2^s * t with t odd
    - For odd n, n - 1 is even, so this factorisation is unique with s >= 1.
    - Goal: compute s and t for several small odd n by hand.
    - [ ] Lab Q9: prove that any z > 0 has a unique decomposition z = 2^s t with t odd.
- [ ] Miller-Rabin observation
    - a^(n-1) mod n = a^(2^s * t) mod n. Build the sequence x_0 = a^t mod n, x_i = x_(i-1)^2 mod n.
    - x_s = a^(n-1) mod n, so the Fermat condition is x_s == 1.
    - Goal: explain how this sequence avoids tracking the binary digits of n - 1.
- [ ] The sequence test
    - If x_s == 1, walk back: each x_i == 1 forces x_(i-1) == +1 or -1 mod n by Theorem 3. Any violation means composite.
    - Subtle point: x_i is in [0, n-1], so x_(i-1) == -1 is checked as x_(i-1) == n - 1.
    - Goal: write out the test conditions for declaring composite vs probably prime.
    - [ ] Lab Q11: work through one Miller-Rabin iteration on n = 21 with a = 13.
- [ ] Strong pseudoprimes and accuracy
    - No analog of Carmichael numbers for Miller-Rabin: at most n/4 witnesses lie for any composite n.
    - With k random witnesses, error probability is at most (1/4)^k.
    - Goal: state the accuracy bound and explain why doubling k roughly squares the confidence.
- [ ] Implementation
    - File target: `src/miller_rabin.py`.
    - Goal: implement, then generate the first 10,000 primes; spot-check against a known list.
    - [ ] Lab Impl 2: implement Miller-Rabin and generate the first 10,000 primes.

---

## 8. Big picture

- [ ] Hierarchy of tests
    - Trial division (slow, exact) -> Fermat (fast, fooled by Carmichael) -> Miller-Rabin (fast, robust).
    - Goal: explain the trade each step makes between speed, exactness, and which composites slip through.
- [ ] Why probabilistic is acceptable
    - Goal: justify in one sentence using the (1/4)^k bound and the cost of a wrong answer in RSA key generation.
- [ ] Connection back to Karatsuba
    - Repeated squaring spends almost all its time inside multiplications mod n; faster multiplication directly speeds up primality testing on big numbers.
    - Goal: state where Karatsuba would slot into a real implementation of Miller-Rabin for cryptographic-sized n.

---

## 9. Implementation milestones, summarised

A re-listing of the implementation steps in order, each pointing at the section above where the theory lives.

- [X] Step 1: Karatsuba multiplication, `src/karatsuba.py` (Section 1, Lab Impl 3).
- [x] Step 2: modular exponentiation by repeated squaring, `src/modular_exponentiation.py` (Section 3, Lab Impl 1). Test against Python's `pow(a, b, n)`.
- [x] Step 3: Fermat randomised test, `src/fermat_test.py` (Section 5). Verify it is fooled by 561 with witness a = 7, then catches it with a = 3.
- [ ] Step 4: Miller-Rabin primality test, `src/miller_rabin.py` (Section 7, Lab Impl 2). Generate the first 10,000 primes; spot-check against a known list.
- [ ] Step 5 (stretch): swap the multiplication backend in steps 2-4 to use `karatsuba.py`. Confirm correctness, then time it against Python `pow` on cryptographic-sized inputs (Section 8).
