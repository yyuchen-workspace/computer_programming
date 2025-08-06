#include <stdio.h>

int main() {
    int digit;
    int count = 0;
    int evensum = 0, oddsum = 0;

    while (scanf_s("%d", &digit) != EOF) {
        if (count % 2 == 0) {
            evensum += digit;
        }
        else {
            oddsum += digit;
        }
        count++;
    }

    int diff = evensum - oddsum;

    if (diff < 0) {
        diff = -diff;
    }

    printf("%d\n", diff % 11 == 0);

    return 0;
}
