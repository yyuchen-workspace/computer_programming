#include <stdio.h>

int main() {
    unsigned int number;
    scanf("%u", &number);

    int n = number & (1 << 4) - 1;
    int k = (number >> 28) & (1 << 4) - 1;

    int secret = (number >> k) & ((1 << n) - 1);

    printf("%d\n", secret);
    return 0;
}
