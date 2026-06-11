# Week 6 Moodle Quiz

Topic: semi-numerical algorithms, Karatsuba multiplication, modular exponentiation, Fermat testing, and Miller-Rabin.

## Questions

1. Addition of two integers is always an `O(1)` operation regardless of input size.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

For arbitrary-size integers, addition depends on the number of digits/bits. Adding two `n`-digit integers takes `O(n)` primitive work.

</details>

---

2. Long multiplication of two `n`-digit integers requires `O(n^2)` primitive operations.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Each digit of one number is multiplied against each digit of the other number.

</details>

---

3. Karatsuba multiplication reduces the number of recursive multiplications from four to three.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The middle cross term is recovered using one extra combined product, so each level uses `3` half-size multiplications instead of `4`.

</details>

---

4. If `a == b (mod n)`, then `a` and `b` must be equal.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

They only need to differ by a multiple of `n`. For example, `3 == 8 (mod 5)`, but `3 != 8`.

</details>

---

5. If `a == b (mod n)`, then `a^k == b^k (mod n)` for any integer `k >= 1`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Congruence is preserved under multiplication, so multiplying the congruence by itself `k` times preserves it under exponentiation.

</details>

---

6. Repeated squaring avoids computing large intermediate values by applying modulo at each step.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The product-mod property lets us reduce after each multiplication, keeping values bounded by the modulus.

</details>

---

7. Naive modular exponentiation runs in polynomial time in the number of bits of the exponent.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Naively doing `b` multiplications is exponential in the bit-length of `b`, because a `d`-bit exponent can have value about `2^d`.

</details>

---

8. Fermat's Little Theorem provides both necessary and sufficient conditions for primality.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

For primes the Fermat congruence holds, but some composite numbers also pass for some bases. These are pseudoprimes.

</details>

---

9. There exist composite numbers that satisfy `a^(n-1) == 1 (mod n)` for some values of `a`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Such composites are pseudoprimes to that base, and the base is called a Fermat liar.

</details>

---

10. If Miller-Rabin declares a number composite, the result is always correct.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Miller-Rabin can incorrectly say "probably prime", but a composite result comes from finding a real witness of compositeness.

</details>

---

11. What determines the time complexity of arithmetic operations in semi-numerical algorithms?

- [ ] a. Value of the numbers
- [ ] b. Number of digits/bit-length
- [ ] c. Base of representation
- [ ] d. Hardware speed

<details>
<summary>Answer</summary>

b. Number of digits/bit-length.

In this unit, arithmetic cost is measured by how many digits/bits must be processed, not by treating arithmetic as constant time.

</details>

---

12. What is the recurrence relation for Karatsuba multiplication?

- [ ] a. `T(n) = 2T(n/2) + O(n)`
- [ ] b. `T(n) = 3T(n/2) + O(n)`
- [ ] c. `T(n) = 4T(n/2) + O(n)`
- [ ] d. `T(n) = T(n/2) + O(n^2)`

<details>
<summary>Answer</summary>

b. `T(n) = 3T(n/2) + O(n)`.

There are three recursive half-size multiplications, plus linear work for splitting, additions, subtractions, and shifts.

</details>

---

13. Which condition is equivalent to `a == b (mod n)`?

- [ ] a. `a = b`
- [ ] b. `a - b` is divisible by `n`
- [ ] c. `a / n = b / n`
- [ ] d. `a mod b = n`

<details>
<summary>Answer</summary>

b. `a - b` is divisible by `n`.

This is the definition of congruence modulo `n`.

</details>

---

14. Why is repeated squaring efficient?

- [ ] a. Reduces exponent size linearly
- [ ] b. Avoids multiplication
- [ ] c. Reduces number of multiplications to `O(log b)`
- [ ] d. Eliminates modulo operation

<details>
<summary>Answer</summary>

c. Reduces number of multiplications to `O(log b)`.

The exponent is handled through its binary representation, so we do work proportional to the number of bits in `b`.

</details>

---

15. Which identity is fundamental to modular exponentiation?

- [ ] a. `(x + y) mod n = (x mod n) + y`
- [ ] b. `(xy) mod n = ((x mod n)(y mod n)) mod n`
- [ ] c. `x^y mod n = x^(y mod n)`
- [ ] d. `n mod x = x mod n`

<details>
<summary>Answer</summary>

b. `(xy) mod n = ((x mod n)(y mod n)) mod n`.

This lets us reduce after each multiplication without changing the final modular result.

</details>

---

16. What is the worst-case time complexity of naive primality testing?

- [ ] a. `O(n)`
- [ ] b. `O(n log n)`
- [ ] c. `O(n d^2)`
- [ ] d. `O(d^2)`

<details>
<summary>Answer</summary>

c. `O(n d^2)`.

Trial division can try `O(n)` possible divisors, and each division on `d`-digit numbers costs `O(d^2)`.

</details>

---

17. What does Fermat's test conclude if `a^(n-1) mod n != 1`?

- [ ] a. `n` is prime
- [ ] b. `n` is composite
- [ ] c. `n` is pseudoprime
- [ ] d. Test is inconclusive

<details>
<summary>Answer</summary>

b. `n` is composite.

If the Fermat condition fails, `n` cannot be prime.

</details>

---

18. What is a Fermat liar?

- [ ] a. A prime number
- [ ] b. A witness proving compositeness
- [ ] c. A base that incorrectly suggests primality
- [ ] d. A divisor of `n`

<details>
<summary>Answer</summary>

c. A base that incorrectly suggests primality.

For composite `n`, a Fermat liar is a base `a` where `a^(n-1) == 1 (mod n)` still holds.

</details>

---

19. Why is `n - 1` written as `2^s * t` in Miller-Rabin?

- [ ] a. To simplify division
- [ ] b. To enable repeated squaring structure
- [ ] c. To reduce `n`
- [ ] d. To find factors directly

<details>
<summary>Answer</summary>

b. To enable repeated squaring structure.

Writing `n - 1 = 2^s t` lets Miller-Rabin compute `a^t, a^(2t), a^(4t), ...` by repeated squaring.

</details>

---

20. What is the error probability after `k` independent Miller-Rabin tests?

- [ ] a. `1 / 2^k`
- [ ] b. `1 / 3^k`
- [ ] c. `1 / 4^k`
- [ ] d. `1 / n^k`

<details>
<summary>Answer</summary>

c. `1 / 4^k`.

For any composite `n`, at most one quarter of bases are strong liars, so independent tests reduce the false-positive probability to at most `(1/4)^k`.

</details>
