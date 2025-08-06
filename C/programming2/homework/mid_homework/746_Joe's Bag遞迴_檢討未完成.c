#include <stdio.h>

int countCombinations(int coins[], int n, int k, int index) {
    // 基本情況：當目標金額為0，表示找到一個組合
    if (k == 0) {
        return 1;
    }

    // 基本情況：當目標金額小於0或沒有更多袋子可選，表示這條路徑無效
    if (k < 0 || index == n) {
        return 0;
    }

    // 選擇當前袋子，並繼續遞迴
    int includeCurrent = countCombinations(coins, n, k - coins[index], index + 1);

    // 不選擇當前袋子，並繼續遞迴
    int excludeCurrent = countCombinations(coins, n, k, index + 1);

    // 返回選擇或不選擇的結果之和
    return includeCurrent + excludeCurrent;
}

int main() {
    int n, k;
    scanf("%d", &n);  // 讀取袋子的數量
    int coins[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &coins[i]);  // 讀取每個袋子中的金額
    }
    scanf("%d", &k);  // 讀取筆記本的價格

    // 從第0個袋子開始遞迴，並尋找所有可能的組合
    int result = countCombinations(coins, n, k, 0);

    // 輸出結果
    printf("%d\n", result);

    return 0;
}

