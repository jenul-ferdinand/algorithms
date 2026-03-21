#include <stdio.h>
#define MIN(a, b) ((a) < (b) ? (a) : (b))

int main() {
    const char string[] = "abaaba";
    const size_t n = sizeof(string) - 1;  // 6 elements

    int z[n];
    for (size_t i = 0; i < n; i++) z[i] = 0;
    z[0] = n;

    int left = -1;
    int right = -1;

    // naive
    for (int k = 1; k < n; k++) {
        if (k > right) {
            // case 1 naive comparison
            size_t j = 0;
            while (k + j < n && string[j] == string[k + j]) {
                j++;
            }
            z[k] = j;
            if (z[k] > 0) {
                left = k;
                right = k + z[k];
            }
        } else if (k <= right) {
            // case 2a or 2b
            z[k] = MIN(z[k - left], right - k);
            // case 2c naive extension
            if (z[k - left] == right - k) {
                size_t m = 0;
                while (right - m < n &&
                       string[right + m] == string[right - k + m]) {
                    m++;
                }
                z[k] += m;
                if (z[k] > 0) {
                    left = k;
                    right = k + z[k];
                }
            }
        }
    }

    // print array
    printf("[");
    for (int m = 0; m < n; m++) {
        printf("%d", z[m]);
        if (m < n - 1) {
            printf(", ");
        }
    }
    printf("]");

    return 0;
}
