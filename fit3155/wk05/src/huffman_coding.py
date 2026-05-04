import bisect


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right


def huffman_code(string):
    """
    Encode a string using Huffman prefix-free coding.

    The algorithm builds a binary tree where each leaf is a character.
    Frequent characters tend to end up closer to the root, giving them
    shorter bit strings. Infrequent characters tend to end up deeper,
    giving them longer bit strings.

    Steps:
    - Count how often each character appears.
    - Create a forest of one-node trees, one tree per character.
    - Keep the forest sorted by frequency.
    - While more than one tree remains:
        - Take the two least frequent trees.
        - Merge them under a new parent whose frequency is their sum.
        - Insert the parent back into the sorted forest.
    - The single remaining tree is the Huffman tree.
    - Walk from the root to each leaf to create the character codes:
        - A left edge adds "0" to the path.
        - A right edge adds "1" to the path.
        - The full root-to-leaf path is that character's code.
        - If there is only one unique character, use "0" as its code.
    - Replace each character in the original string with its code.
    """
    # get frequencies
    freq = {c: 0 for c in string}
    for c in string:
        freq[c] += 1
    charset = freq.keys()

    # initial forest
    forest: list[Node] = []
    for char in charset:
        node = Node(freq=freq[char], char=char)
        bisect.insort(forest, node, key=lambda x: x.freq)

    # merging into parent
    parent: Node = None
    while len(forest) > 1:
        left = forest[0]
        right = forest[1]
        freq = left.freq + right.freq
        parent = Node(freq=freq, left=left, right=right)
        forest = forest[2:]
        bisect.insort(forest, parent, key=lambda x: x.freq)

    # build codes
    def build_codes(node: Node, path: str):
        if node.char is not None:
            codes[node.char] = path or "0"
            return

        build_codes(node.left, path + "0")
        build_codes(node.right, path + "1")

    codes = {}
    build_codes(node=forest[0], path="")

    # build encoded
    return "".join(codes[c] for c in string)


if __name__ == "__main__":
    string = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    encoded = huffman_code(string)
    assert (
        encoded
        == "1000011101001000110010011101100111001001000111110010011111011111100010001111110100111001001011111011101000111111001"
    )
