
#include <stdio.h>

typedef struct {
    int n;
} Frame;

#define MAX 100
Frame stack[MAX];
int top = -1;

int factorial(int n) {
    int result = 1;
    while (n > 1) {
        stack[++top].n = n--;
    }
    while (top != -1) {
        result *= stack[top--].n;
    }
    return result;
}

int main() {
    int n = 5;
    printf("factorial(%d) = %d\n", n, factorial(n));
    return 0;
}
