"""
Fixed-length coding helpers.

In a fixed-length code, every character is represented using the same
number of bits. This makes decoding simple: split the bit stream into
equal-sized chunks, then convert each chunk back to a character.

Assumed ASCII range for the examples: [37, 126].
"""

def flc_encode(string: str, bit_width: int = 8):
    """
    Encode a string using fixed-length binary codewords.

    Each character is treated independently:
    - Convert the character to its ASCII/Unicode integer value with ord().
    - Convert that integer to binary.
    - Pad the binary representation with leading zeroes so every codeword
      has the same width.
    - Join all fixed-width codewords into one bit string.

    Because every codeword has the same width, the decoder does not need a
    tree or separator symbols. It only needs to know the chosen bit width.
    The bit width must be large enough to store every character value.
    """
    binaries = []

    for c in string:
        binary = bin(ord(c))[2:]
        padding = bit_width - len(binary)
        codeword = "0" * padding + binary
        binaries.append(codeword)

    return "".join(binaries)


def bin_to_int(byte: str) -> int:
    """
    Convert a binary string into its integer value.

    The leftmost bit has the largest power-of-two weight. For example,
    "101" is read as 1*4 + 0*2 + 1*1 = 5.
    """
    m = len(byte)
    weights = [2**i for i in reversed(range(m))]
    bits = [int(b) for b in byte]

    nums = []
    for j in range(m):
        nums.append(bits[j] * weights[j])

    return sum(nums)


def flc_decode(code: str, bit_width: int = 8):
    """
    Decode a fixed-length binary code back into a string.

    The code is readable because all encoded characters occupy the same
    number of bits.

    Steps:
    - Split the bit string into equal-width chunks.
    - Convert each binary chunk back into an integer.
    - Convert each integer back into a character with chr().
    - Join the characters to recover the original string.
    """
    n = len(code)
    bins = []
    for i in range(0, n, bit_width):
        binary = code[i : i + bit_width]
        bins.append(binary)

    ords = []
    for binary in bins:
        num = bin_to_int(binary)
        ords.append(num)

    encoded = ""
    for o in ords:
        c = chr(o)
        encoded = encoded + c

    return encoded

if __name__ == "__main__":
    string = "%foo"
    encoded = flc_encode(string)
    decoded = flc_decode(encoded)
    assert decoded == string
