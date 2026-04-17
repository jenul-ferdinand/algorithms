def suffix_array_prefix_doubling(string: str) -> list[int]:
    if string[-1] != "$":
        string = string + "$"

    n = len(string)

    # Build the array of all suffixes and the ranks array
    rank = [-1] * n
    suffix = list(range(n))
    rank = [ord(string[i]) for i in range(n)]

    # Run logn rounds
    k = 1
    while k < n:
        # Sort based on rank as sort key
        suffix.sort(
            key=lambda i: (rank[i], rank[i + k]) if i + k < n else (rank[i], -1)
        )

        # Assign new rankings
        new_rank = [0] * n
        counter = 0
        for i in range(n):
            if i == 0:
                new_rank[suffix[i]] = 0
                continue

            previous = (
                (rank[suffix[i - 1]], rank[suffix[i - 1] + k])
                if suffix[i - 1] + k < n
                else (rank[suffix[i - 1]], -1)
            )
            current = (
                (rank[suffix[i]], rank[suffix[i] + k])
                if suffix[i] + k < n
                else (rank[suffix[i]], -1)
            )

            if previous != current:
                counter += 1
                new_rank[suffix[i]] = counter

            else:
                new_rank[suffix[i]] = counter

        rank = new_rank

        k *= 2

    return suffix
