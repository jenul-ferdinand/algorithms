# Week 5: Lossless data compression - Learning Roadmap

Source material: `seminar05.pdf` (43 slides), `lab05.pdf`, plus the recommended reading from slide 4 (MacKay, _Information Theory, Inference and Learning Algorithms_, ch. 1; Sayood, _Introduction to Data Compression_, ch. 3 and 5).
Note: there is no `notes05.pdf` for this week. The seminar slides serve as the primary written reference.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab05.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. What compression is and why it works

- [x] Definition: lossless data compression
    - Encoder produces a compact bitstream from data; decoder perfectly reconstructs the original. No information is discarded.
    - Goal: state the diagram (data -> Encoder -> encoded -> Decoder -> data) and contrast with lossy compression (JPEG, MP3).
- [x] Compression = signal + noise decomposition
    - data = redundant + random = compressible + uncompressible = model + deviations.
    - Goal: explain in one sentence why purely random data cannot be compressed.
- [x] Frequency drives compressibility
    - Frequent symbols deserve short codewords; rare ones deserve long ones. The ranking of letter frequencies in English (e, t, a, o, i, n, s, h, r, ...) is a worked example.
    - Goal: argue why uniform distributions admit no compression beyond log2(n) bits per symbol.
- [ ] Shannon's information content (per LEARNING_INTENTIONS)
    - I(x) = -log2 P(x) bits. The information of a symbol is large when its probability is small.
    - Goal: state the formula and compute I(x) for P(x) = 1/2, 1/4, 1/8.
- [ ] Shannon entropy
    - H(X) = sum over x of P(x) * I(x) = -sum P(x) log2 P(x).
    - Goal: state the formula. Compute H for a fair coin (1 bit) and for a biased coin with P = 0.9 (~0.47 bits).
- [ ] Entropy as the lower bound on average codeword length
    - Any uniquely decodable code over X has expected length >= H(X). Huffman achieves H(X) <= L < H(X) + 1.
    - Goal: state the bound and explain why Huffman is "near-optimal" but not always exactly optimal (the +1 gap closes via arithmetic coding, but that is out of scope).

---

## 2. Fixed-length codes (FLC)

- [x] What an FLC is
    - Every symbol gets a codeword of the same bit width w. Decode by splitting the stream into w-bit chunks.
    - Goal: state when w must be at least ceil(log2 |sigma|).
- [x] ASCII as the canonical FLC
    - 7-bit (or 8-bit padded) per character, no compression for non-uniform input. Frequency-blind.
    - Goal: explain why ASCII is information-theoretically wasteful for English text.
- [x] Impl: FLC encoder/decoder (`src/flc.py`).
    - Round-trip a string at arbitrary bit width.

---

## 3. Variable-length codes and the ambiguity problem

- [x] Why varying lengths
    - Shorter codewords for frequent symbols, longer for rare. Total bits go down, on average.
    - Goal: redo the Morse-code intuition (slide 12). E (most frequent) gets a single dot.
- [x] The ambiguity demo
    - With A=0, B=1, C=10, D=101, the bitstream `1010` decodes as BABA, CC, or DA. Not uniquely decodable.
    - Goal: explain why the ambiguity comes from one codeword being a prefix of another.
- [x] Prefix-free (a.k.a. instantaneous) codes
    - No codeword is a prefix of another. Encoded streams are uniquely decodable, and the decoder can decode each symbol the moment its full codeword is consumed.
    - Goal: state the property and verify A=0, B=10, C=110, D=111 satisfies it.

---

## 4. Huffman coding

- [x] Definition: Huffman code
    - Greedy bottom-up tree construction. Repeatedly merge the two least-frequent subtrees into a new internal node whose frequency is their sum. Codeword for each symbol = root-to-leaf path (left=0, right=1).
    - Goal: write the construction algorithm in pseudocode (5 lines).
- [x] Worked example: `A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED`
    - Frequencies: A=11, _=10, D=10, E=7, B=6, C=2. Build tree, derive codewords (slide 17 trace).
    - Goal: hand-build the tree and reproduce the codewords _=00, A=01, E=110, C=1110, B=1111.
- [x] Construction summary (slide 18)
    - Convention: lower frequency goes left (bit 0), higher goes right (bit 1). Ties broken arbitrarily by default.
    - Goal: state the convention.
- [x] Optimality proof (greedy choice, slide 19)
    - Merging the two lowest-frequency symbols psi_1 and psi_2 first is optimal. Any swap with a higher-frequency symbol increases L(n). Hence L(n) = L(n-1) + f_1 + f_2; minimising L(n-1) recursively gives the optimum.
    - Goal: reproduce the exchange argument.
- [x] Lab Q1(a): total encoded bits
    - Total bits = sum over i of f_i * l_i, where l_i is the codeword length of symbol s_i.
    - Goal: state the formula.
- [x] Lab Q1(b): can a non-leaf-1, non-leaf-2 symbol have l_i > l_1?
    - No. The two least frequent symbols are merged first and end up at the deepest level. Any other symbol has l_i <= max(l_1, l_2) = l_1 = l_2.
    - Goal: prove via the merge-order invariant.
- [x] Lab Q1(c): min and max possible l_i
    - Min: 1 bit (only achievable if there are exactly 2 symbols, or a degenerate tree with one symbol uses 1 bit by convention).
    - Max: n - 1 bits (skewed tree where each merge adds a leaf at the next level).
    - Goal: state both bounds and produce a frequency distribution (e.g. Fibonacci-like) that achieves the n - 1 max.
- [ ] Lab Q1(d): can a Huffman tree have height < ceil(log2 n)?
    - No. A binary tree with n leaves has height >= ceil(log2 n). The lower bound is achieved by a balanced tree, which Huffman produces when all frequencies are equal.
    - Goal: justify via the leaf-count vs height inequality 2^h >= n.
- [ ] Lab Q2: Huffman for {a, b, c, d, e} with probs {0.4, 0.2, 0.2, 0.1, 0.1}
    - Goal: build the tree by hand and report the codeword set.
- [ ] Lab Q3: minimum-variance Huffman
    - Tie-break by minimum subtree height, not arbitrary choice. Re-do Q2 under this rule and compare codewords.
    - Goal: produce both codeword sets side by side and observe that minimum-variance keeps codeword lengths closer to each other.
- [ ] Lab Q4: is Huffman always prefix-free?
    - Yes. Codewords correspond to root-to-leaf paths in a binary tree where each leaf is a symbol. No leaf is on the path to another leaf, so no codeword is a prefix of another.
    - Goal: state this in one paragraph as a tree-property argument.
- [x] Impl: Huffman encoder (`src/huffman_coding.py`).
    - Frequency dict, sorted forest of nodes, iterative merge, root-to-leaf codeword extraction. Produces the canonical bitstream from slide 17.

---

## 5. Prefix-free codes for integers (Elias omega)

- [x] Why we need a separate code for integers
    - Huffman is impractical when the alphabet is `Z+` (unbounded) or when integers in the stream are nearly unique. We want a self-delimiting binary code for arbitrary positive integers.
    - Goal: state in one sentence why Huffman is unsuitable for "send me an arbitrary positive integer".
- [x] Definition: minimal binary code
    - The binary representation of N with no leading zeros, i.e. starts with 1. Has length floor(log2 N) + 1.
    - Goal: write the minimal binary code of 561 (it is `1000110001`, 10 bits).
- [x] Naive concatenation breaks decoding
    - Concatenating minimal binary codes of N, L_1, L_2, ... does not yield a self-delimiting stream because every component starts with 1 and the boundaries are invisible.
    - Goal: walk slide 23 and explain why the concatenation `11110011000110001` of 561 cannot be uniquely parsed.
- [x] The Elias omega construction
    - Start from N. Compute L_1 = length(binary(N)) - 1. Then L_2 = length(binary(L_1)) - 1. Continue until length(binary(L_k)) = 1.
    - Concatenate L_k, L_{k-1}, ..., L_1, N (each in minimal binary), but with the most significant bit of every length component flipped from 1 to 0.
    - The terminal code component (N itself) keeps its leading 1.
    - Goal: write the bit layout from memory.
- [x] Decoding rule
    - Read bit by bit. On a 0 you are inside a length component; that 0 represents what would have been a 1, and the remainder of that component encodes a length. On the first 1, you are at the start of the code component N (whose length is determined by the most recently decoded length).
    - Goal: walk through decoding 561 from its omega code by hand.
- [ ] Lab Q5: Elias omega codewords for 65535 and 65536
    - 65535 = 2^16 - 1 has minimal binary `1111111111111111` (16 bits). 65536 = 2^16 has minimal binary `10000000000000000` (17 bits).
    - Build both codewords end to end and decode each back.
    - Goal: produce both codewords; observe how 65536 needs an extra length component compared to 65535.
- [ ] Lab Q6: when does the number of length components increase?
    - The count of length components grows by one when the bit length of the previous outermost length component itself crosses a power-of-two boundary. Specifically: when N first reaches a value where length(binary(N)) - 1 has more bits than for N - 1.
    - Goal: write the rule and confirm it on the 65535 -> 65536 transition (length jumps from 16 to 17, length(binary(16)) = 5 vs length(binary(15)) = 4, triggering an extra component).
- [ ] Impl: Elias omega encoder/decoder. New file `src/elias_omega.py`.
    - Goal: round-trip every integer in [1, 100000].

---

## 6. LZ77

- [x] Sliding window dictionary compression
    - Maintain a search window (the most recent W characters already encoded) and a lookahead buffer (the next L characters to encode). Find the longest prefix of the lookahead buffer that occurs in the window. Emit a triple <offset, length, next_char>.
    - Goal: state the three components of an LZ77 triple and explain what each means: offset = how far back in the window the match starts; length = how many characters match; next_char = the character that follows the match in the lookahead.
- [x] Encoder loop
    - 1. Find longest match between window and lookahead.
    - 2. Emit <offset, length, lookahead[length]> (note: the next_char is included even if length = 0, so each triple advances at least one character).
    - 3. Slide both window and lookahead forward by length + 1.
    - Goal: write the loop in pseudocode.
- [x] Decoder loop
    - For each triple <offset, length, ch>: copy `length` characters starting `offset` positions back from the current end of the output, then append `ch`.
    - Goal: walk a small example (e.g. encode and decode `aabaab`).
- [ ] Lab Q7: LZ77 encode `b a r r a y a r _ b a r _ b y _ b a r r a y a r _ b a y` with W = L = 15
    - Goal: produce the full triple sequence.
- [ ] Lab Q8: decode the Q7 triples
    - Goal: confirm that decoding recovers the original string.
- [ ] Lab Q10: decode <0,0,r>, <0,0,a>, <0,0,t>, <2,8,_>, <3,1,_>, <0,0,r>, <6,4,t>, <9,5,t>
    - Goal: produce the recovered string. The first three triples seed the dictionary; subsequent triples copy from earlier output.
- [ ] Window size tradeoffs
    - Larger W finds more matches but increases offset bit-width. Larger L finds longer matches but increases length bit-width. Practical implementations cap both.
    - Goal: state the tradeoff and identify why offset and length both need to fit in bounded codewords.
- [ ] Impl: LZ77 encoder/decoder. New file `src/lz77.py`.
    - Goal: round-trip arbitrary ASCII inputs at fixed (W, L). Verify against the Q7/Q8 expected output.

---

## 7. LZSS variant

- [x] What LZSS changes
    - LZSS emits either a literal character or a back-reference <offset, length>, never both in the same token. A 1-bit flag distinguishes the two. Avoids wasting the `next_char` field when no match is found.
    - Goal: explain why this is more efficient than LZ77 when matches are common but the trailing literal is wasteful.
- [x] Encoder loop
    - 1. Find longest match. If length >= some threshold (typically 3, since a 1-bit flag + 2-byte reference must beat 1 byte raw), emit <flag=1, offset, length>. Otherwise emit <flag=0, char>.
    - 2. Advance by length (for matches) or by 1 (for literals).
    - Goal: state the threshold rule and write the pseudocode.
- [ ] Lab Q9: LZSS encode and decode the Q7 string with W = L = infinity
    - With unbounded window/buffer, every prefix of the lookahead can match anywhere in the prefix of the text. This gives the maximum-compression case.
    - Goal: produce the LZSS token sequence and confirm decoding round-trips.
- [ ] Impl: LZSS encoder/decoder. New file `src/lzss.py`.
    - Goal: round-trip and compare compressed byte counts against `lz77.py` on a few inputs.

---

## 8. Putting it together: a real compressed file format

- [ ] Lab Impl Q1: end-to-end Huffman + Elias omega ASCII compressor
    - Output binary file structure:
        - (a) Number of distinct characters, Elias omega encoded.
        - (b) For each character: its frequency (Elias omega encoded), then its ASCII code (8 bits).
        - (c) Total number of characters, Elias omega encoded.
        - (d) Huffman-encoded bitstream of the text, padded to byte boundary.
    - Decoder reverses the process.
    - Files: `src/huffman_compressor.py`, `src/huffman_decompressor.py`.
    - Goal: round-trip `lab05.pdf` itself (or any ASCII file) and report compression ratio.
- [ ] Lab Impl Q2: LZ77 file format
    - Identify what header metadata is required: window size W, lookahead size L, number of triples, encoding scheme for offset/length/character.
    - Files: `src/lz77_compressor.py`, `src/lz77_decompressor.py`.
    - Goal: round-trip a real file. Report compression ratio.
- [ ] Lab Impl Q3: LZSS file format
    - Same exercise, with the 1-bit literal/reference flag and the match-threshold rule.
    - Files: `src/lzss_compressor.py`, `src/lzss_decompressor.py`.
    - Goal: round-trip and compare ratio to `lz77`.

---

## 9. Implementation milestones, summarised

A re-listing of the implementation steps in order. Files live in `src/`.

- [x] Step 1: fixed-length code (`src/flc.py`).
- [x] Step 2: Huffman encoder (`src/huffman_coding.py`).
- [ ] Step 3: Huffman decoder. Either extend `huffman_coding.py` or add `src/huffman_decoder.py`. Needs to consume the bitstream plus the codeword table.
- [ ] Step 4: Elias omega encoder/decoder (`src/elias_omega.py`). Round-trip every N in [1, 100000].
- [ ] Step 5: LZ77 encoder/decoder (`src/lz77.py`). Verify against Lab Q7/Q8 expected output.
- [ ] Step 6: LZSS encoder/decoder (`src/lzss.py`).
- [ ] Step 7: end-to-end Huffman compressor with Elias omega header (Lab Impl Q1).
- [ ] Step 8: end-to-end LZ77 compressor (Lab Impl Q2).
- [ ] Step 9: end-to-end LZSS compressor (Lab Impl Q3).
- [ ] Step 10 (stretch): compute the empirical entropy of an input file and compare against the Huffman-compressed bit count to see how close to optimal you are.
