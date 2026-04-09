#ifndef PRINTARR_H
#define PRINTARR_H

#include <stdio.h>
#include <stddef.h>

static void printarr(int *arr, size_t n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d", arr[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]");
}

#endif