#include <stdio.h>

int josephus(int n, int m) {
    int res = 0;
    for (int i = 2; i <= n; ++i)
        res = (res + m) % i;
    return res;
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    int winner = (josephus(n, m) + (n - 1)) % n;
    int offset = (winner - (n - 1) + n) % n;

    if (offset == 0) {
        printf("-1\n");
    } else {
        printf("%d\n", offset);
    }

    return 0;
}
