#include <stdio.h>

int main() {
    int N, arr[105];
    scanf("%d", &N);

    for (int i = 0; i < N; i++)
        scanf("%d", &arr[i]);

    int count = 0;

    for (int j = 1; j < N - 1; j++) {
        int left = 0, right = 0;

        // 左邊找比 arr[j] 大的數量
        for (int i = 0; i < j; i++) {
            if (arr[i] > arr[j]) left++;
        }

        // 右邊找比 arr[j] 大的數量
        for (int k = j + 1; k < N; k++) {
            if (arr[k] > arr[j]) right++;
        }

        count += left * right;
    }

    printf("%d\n", count);
    return 0;
}
