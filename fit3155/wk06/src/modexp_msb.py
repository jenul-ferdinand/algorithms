def modexp_msb(a: int, b: int, n: int):
    """
    Modular exponentiation from MSB to LSB

    Rules per bit
    Let r be the previous bit computation result
    (rule one) R_1 = r * r mod n
    (rule two) R_2 = R_1 * a mod n
    """
    b = bin(b)[2:]

    r = 1
    for x in b:
        R_1 = (r * r) % n # rule one
        r = R_1
        if x == "1":
            R_2 = R_1 * a % n # rule two
            r = R_2

    return r


if __name__ == "__main__":
    r = modexp_msb(7, 560, 561)
    print("result", r)
