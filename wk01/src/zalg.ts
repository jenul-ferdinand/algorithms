const zalg = (string: string): number[] => {
    const n = string.length;
    let z = Array(n).fill(0);
    z[0] = n;
    let l = -1;
    let r = -1;
    z.forEach((_, k) => {
        if (k > r) {
            let i = 0;
            while (k + i < n && string[i] == string[k + i]) {
                i++;
            }
            z[k] = i;
            if (z[k] > 0) {
                l = k;
                r = k + z[k];
            }
        } else {
            z[k] = Math.min(z[k - l], r - k);

            let i = 0;
            while (r + i < n && string[r + i] == string[r - k + i]) {
                i++;
            }
            z[k] += i;
            if (z[k] > 0) {
                l = k;
                r = k + z[k];
            }
        }
    });

    return z;
};
