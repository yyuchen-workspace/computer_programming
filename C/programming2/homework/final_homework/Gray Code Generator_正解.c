#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    int N = 1 << n;  // 計算 2 的 n 次方

    for (int i = 0; i < N; i++) {
        int gray = i ^ (i >> 1);
        printf("%d ", gray);
    }

    return 0;
}
