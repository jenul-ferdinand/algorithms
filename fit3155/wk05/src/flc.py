"""
Fixed-Length Coding

Assumed ASCII Range: [37, 126]
"""

def flc_encode(string: str, bit_width: int = 8):
    binaries = []

    arr = [c for c in string]
    for c in arr:
        binary = bin(ord(c))[2:]
        padding = bit_width - len(binary)
        codeword = "0" * padding + binary
        binaries.append(codeword)

    for i in range(len(binaries)):
        m = len(binaries[i]) - 1
        offset = bit_width - m

        binaries[i] = "0" * offset + binaries[i]

    return "".join(binaries)


def bin_to_int(byte: str) -> int:
    m = len(byte)
    weights = [2**i for i in reversed(range(m))]
    bits = [int(b) for b in byte]

    nums = []
    for j in range(m):
        nums.append(bits[j] * weights[j])

    return sum(nums)


def flc_decode(code: str, bit_width: int = 8):
    n = len(code)
    bins = []
    for i in range(0, n, bit_width + 1):
        binary = code[i : i + bit_width + 1]
        bins.append(binary)

    ords = []
    for bin in bins:
        num = bin_to_int(bin)
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
