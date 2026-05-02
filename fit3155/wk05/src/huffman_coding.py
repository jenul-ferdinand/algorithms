import bisect


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right


def huffman_code(str):
    """Huffman prefix free coding"""
    freq = {c: 0 for c in str}
    for c in str:
        freq[c] += 1
    charset = freq.keys()

    # initial bst
    bst: list[Node] = []
    for char in charset:
        node = Node(freq=freq[char], char=char)
        bisect.insort(bst, node, key=lambda x: x.freq)

    # merging into parent
    parent = None
    while len(bst) != 1:
        freq = bst[0].freq + bst[1].freq
        parent = Node(freq, left=bst[0], right=bst[1])
        bst = bst[2:]
        bisect.insort(bst, parent, key=lambda x: x.freq)

    # build codes
    codes = {}

    def build_codes(node: Node, path: str):
        if node.char is not None:
            codes[node.char] = path
            return

        build_codes(node.left, path + "0")
        build_codes(node.right, path + "1")

    build_codes(node=parent, path="")

    # build encoded
    encoded = ""
    for c in str:
        encoded = encoded + codes[c]

    return encoded


if __name__ == "__main__":
    string = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    encoded = huffman_code(string)
    assert (
        encoded
        == "1000011101001000110010011101100111001001000111110010011111011111100010001111110100111001001011111011101000111111001"
    )
