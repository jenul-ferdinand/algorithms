#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

bool boyermoore_basic(const char* pat, const char* txt) {
    int n = strlen(txt);
    int m = strlen(pat);

    int rdict[128] = {0};  // init 0s for array of size 128 for all ASCII chars
    for (int i = 0; i < m; i++)
        rdict[(int)pat[i]] = i;  // assign rightmost ocurrence position in pat

    int x = 0;
    while (x <= n - m) {
        int k = m - 1;
        while (k >= 0 && pat[k] == txt[x + k]) {
            k--;
        }

        if (k == -1) return true;

        int rx = rdict[txt[x + k]];
        x += MAX(k - rx, 1);
    }

    return false;
}

int main() {
    const char* txt = "sphoorythy";
    const char* pat = "thy";
    bool res = boyermoore_basic(pat, txt);
    assert(res == true);

    txt = "xyzsomething";
    pat = "abc";
    res = boyermoore_basic(pat, txt);
    assert(res == false);

    txt = "xxxxxxxxxabc";
    pat = "abc";
    res = boyermoore_basic(pat, txt);
    assert(res == true);

    return 0;
}