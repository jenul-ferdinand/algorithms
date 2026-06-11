# Week 5 Moodle Quiz

Topic: lossless data compression, Huffman coding, Elias omega, LZ77, and LZSS.

## Questions

1. All data streams can be compressed arbitrarily well using lossless compression.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Lossless compression only removes redundancy. Purely random or already-compressed data may have no useful redundancy to remove.

</details>

---

2. Fixed-length coding can achieve optimal compression if symbol frequencies are highly skewed.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Fixed-length coding gives every symbol the same number of bits, so it cannot exploit frequent symbols with shorter codewords.

</details>

---

3. Any variable-length code is uniquely decodable as long as no two codewords are identical.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Different codewords are not enough. If one codeword is a prefix of another, the same bitstream may still have multiple parses.

</details>

---

4. If a code is prefix-free, decoding can be done without backtracking.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Once the decoder reaches a complete codeword, no longer codeword can begin with it, so the symbol can be output immediately.

</details>

---

5. Huffman coding always assigns codewords of equal length to symbols with equal frequencies.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Equal frequencies create ties, and tie-breaking can change the final tree shape. Huffman optimises total weighted length, not equal lengths for tied symbols.

</details>

---

6. Merging the two least frequent symbols first is necessary for optimality in Huffman coding.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

In an optimal Huffman tree, the two least frequent symbols can be placed deepest as siblings, so the greedy merge is safe.

</details>

---

7. Huffman coding is efficient for encoding large ranges of nearly unique integers.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

If most integers are unique or the range is unbounded, the Huffman table becomes expensive and there is little frequency advantage.

</details>

---

8. In Elias omega coding, length components are encoded without modification.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

The leading `1` of each length component is flipped to `0`. The final integer component keeps its leading `1`.

</details>

---

9. During Elias omega decoding, encountering a leading `1` indicates termination of decoding.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Length components begin with a flipped `0`; the first leading `1` marks the final integer component.

</details>

---

10. In LZ77, the length of the match can exceed the size of the lookahead buffer.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

The match is a prefix of the lookahead buffer, so its length is bounded by the lookahead size.

</details>

---

11. What fundamentally enables data compression?

- [ ] a. Randomness in data
- [ ] b. Redundancy in data
- [ ] c. Large alphabet size
- [ ] d. Binary encoding

<details>
<summary>Answer</summary>

b. Redundancy in data.

Compression works by replacing repeated or predictable structure with shorter descriptions.

</details>

---

12. Why does LZSS switch encoding format for short matches?

- [ ] a. To improve decoding speed
- [ ] b. To reduce bit overhead
- [ ] c. To simplify implementation
- [ ] d. To increase match length

<details>
<summary>Answer</summary>

b. To reduce bit overhead.

For a short match, a back-reference may cost more bits than just storing the literal character.

</details>

---

13. Why are shorter codewords assigned to frequent symbols?

- [ ] a. To simplify decoding
- [ ] b. To minimize average code length
- [ ] c. To reduce alphabet size
- [ ] d. To avoid ambiguity

<details>
<summary>Answer</summary>

b. To minimize average code length.

The total cost is `sum frequency * codeword_length`, so frequent symbols matter most.

</details>

---

14. Which property ensures unique decodability?

- [ ] a. Equal length
- [ ] b. Prefix-free property
- [ ] c. Binary representation
- [ ] d. Greedy construction

<details>
<summary>Answer</summary>

b. Prefix-free property.

If no codeword is a prefix of another, the decoder can identify each symbol boundary unambiguously.

</details>

---

15. In a Huffman tree, what do internal nodes represent?

- [ ] a. Single characters
- [ ] b. Binary digits
- [ ] c. Subsets of characters
- [ ] d. Leaf frequencies

<details>
<summary>Answer</summary>

c. Subsets of characters.

Each internal node is formed by merging subtrees, so it represents the combined set of symbols below it.

</details>

---

16. Why does assigning longer codes to less frequent symbols reduce total cost?

- [ ] a. They occur less often
- [ ] b. They require fewer bits
- [ ] c. They are easier to decode
- [ ] d. They balance the tree

<details>
<summary>Answer</summary>

a. They occur less often.

A long codeword hurts less when the symbol appears rarely.

</details>

---

17. Why is the leading bit flipped in length components in Elias omega coding?

- [ ] a. To reduce size
- [ ] b. To ensure prefix-free property
- [ ] c. To encode negative numbers
- [ ] d. To align bytes

<details>
<summary>Answer</summary>

b. To ensure prefix-free property.

The flipped leading bit separates length components from the final integer component, making the code self-delimiting.

</details>

---

18. What determines the next segment length during Elias decoding?

- [ ] a. Previous decoded value
- [ ] b. Current segment value + 1
- [ ] c. Remaining bits
- [ ] d. Fixed size

<details>
<summary>Answer</summary>

b. Current segment value + 1.

After decoding a length value `x`, the next segment has `x + 1` bits.

</details>

---

19. What does the offset represent in LZ77?

- [ ] a. Length of match
- [ ] b. Distance back to match
- [ ] c. Position in buffer
- [ ] d. Number of matches

<details>
<summary>Answer</summary>

b. Distance back to match.

The offset says how far back from the current output position the copied text begins.

</details>

---

20. Why is the longest match preferred in LZ77?

- [ ] a. Simplifies decoding
- [ ] b. Maximizes compression efficiency
- [ ] c. Reduces offset size
- [ ] d. Avoids overlap

<details>
<summary>Answer</summary>

b. Maximizes compression efficiency.

A longer match replaces more upcoming characters with one reference, usually improving compression.

</details>
