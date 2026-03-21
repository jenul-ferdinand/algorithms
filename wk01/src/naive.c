#include <stdio.h>

int main() {
    const char string[] = "abxbab";
    const size_t n = sizeof(string) - 1;  // 6 elements

    int z[n];
    for (size_t i = 0; i < n; i++) z[i] = 0;
    z[0] = n;

    // naive
    for (int k = 1; k <= n; k++) {
        size_t j = 0;
        while (k + j < n && string[j] == string[k + j]) {
            j++;
        }
        z[k] = j;
    }

    // print array
    printf("[");
    for (int m = 0; m <= n; m++) {
        printf("%d", z[m]);
        if (m < n) {
            printf(", ");
        }
    }
    printf("]");

    return 0;
}
