const naive = (string: string): number[] => {
    const n: number = string.length;
    let z: number[] = Array(n).fill(0);
    z[0] = n;

    z.forEach((_, k) => {
        let i = 0;
        while (k + i < n && string[i] == string[k + i]) {
            i++;
        }
        return (z[k] = i);
    });

    return z;
};

const z = naive("abxbab");
const correct = [6, 0, 0, 0, 2, 0];
console.assert(
    z.every((v, i) => v === correct[i]),
    `Expected ${correct}, got ${z}`,
);
