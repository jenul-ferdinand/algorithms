# Alphabet range 37 - 126 inclusive
ASCII_LOWER = 37
ASCII_UPPER = 126
TERMINAL_CHAR = "$"
ALPHABET_OFFSET = ord(TERMINAL_CHAR)
ALPHABET_SIZE = ASCII_UPPER - ALPHABET_OFFSET + 1


def ascii_order(c: str):
    if len(c) > 1:
        raise ValueError("Given a string, expected a singular character")

    return ord(c) - ALPHABET_OFFSET
