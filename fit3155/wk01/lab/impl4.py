
def zalg(string: str) -> list[int]:  
    n = len(string)
    z = [0] * n
    z[0] = n
    left, right = -1, -1
    for k in range(1, n):
        if k > right:
            i = 0
            while k + i < n and string[i] == string[k + i]:
                i += 1
            z[k] = i
            if z[k] > 0:
                left = k
                right = k + z[k]
        if k <= right:
            z[k] = min(z[k - left], right - k)

            if z[k - left] == right - k:
                i = 0
                while right + i < n and string[right + i] == string[right - k + i]:
                    i += 1
                z[k] += i
                if z[k] > 0:
                    left = k
                    right = k + z[k]

    return z

def zalgmatcher(pattern: str, string: str) -> list[bool]:
    """
    Matches some pattern with a string giving an array of size P where True 
    values indicate a full pattern match.

    P is the length of the pattern.
    """
    patstring = pattern + '$' + string
    seplen = len(pattern)+1
    patlen = len(pattern)
    strlen = len(string)

    z = zalg(patstring)
    return [z[i] == patlen for i in range(seplen, strlen)]

if __name__ == '__main__':
    matcharr = zalgmatcher('ab', 'ababab')
    answer = [True, False, True, False, True, False]
    assert matcharr == answer, f'\nExpected: {answer}\nGot: {matcharr}'