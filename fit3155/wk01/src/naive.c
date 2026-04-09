#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <printarr.h>
#include <assert.h>

int* naive(const char* string, size_t* out_n) {
    size_t n = strlen(string);
    int* z = calloc(n, sizeof(int));  // allocate on heap with zeros
    z[0] = n;

    for (int k = 1; k < n; k++) {
        size_t i = 0;
        while (k + i < n && string[i] == string[k + i]) {
            i++;
        }
        z[k] = i;
    }

    *out_n = n;  // writing length back to caller
    return z;
}

int main() {
    const char string[] = "abxbab";

    size_t n;
    int* z = naive(string, &n);

    printarr(z, n);
    int expected[] = {6,0,0,0,2,0};
    assert(memcmp(z, expected, n * sizeof(int)) == 0);

    free(z); // free stored z array from heap

    return 0;
}
