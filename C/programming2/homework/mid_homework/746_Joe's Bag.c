#include <stdio.h>

#define MAX_K 10000

int main() {
    int n, k;
    scanf("%d", &n);  // 讀取袋子的數量
    int coins[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &coins[i]);  // 讀取每個袋子中的金額
    }
    scanf("%d", &k);  // 讀取筆記本的價格

    // dp[j]表示能組合出金額j的方式數量
    int dp[k + 1];
    for (int i = 0; i <= k; i++) {
        dp[i] = 0;  // 初始化dp數組
    }
    dp[0] = 1;  // dp[0]表示金額為0的組合方式有1種（不選任何袋子）

    // 動態規劃過程
    for (int i = 0; i < n; i++) {
        for (int j = k; j >= coins[i]; j--) {
            dp[j] += dp[j - coins[i]];  // 更新dp[j]
        }
    }

    // 輸出最終結果，dp[k]表示能組合出金額k的方式數量
    printf("%d\n", dp[k]);

    return 0;
}
