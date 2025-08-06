#include <stdio.h>

#define MAX_K 10000

int main() {
    int n, k;
    scanf("%d", &n);  // Ū���U�l���ƶq
    int coins[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &coins[i]);  // Ū���C�ӳU�l�������B
    }
    scanf("%d", &k);  // Ū�����O��������

    // dp[j]��ܯ�զX�X���Bj���覡�ƶq
    int dp[k + 1];
    for (int i = 0; i <= k; i++) {
        dp[i] = 0;  // ��l��dp�Ʋ�
    }
    dp[0] = 1;  // dp[0]��ܪ��B��0���զX�覡��1�ء]�������U�l�^

    // �ʺA�W���L�{
    for (int i = 0; i < n; i++) {
        for (int j = k; j >= coins[i]; j--) {
            dp[j] += dp[j - coins[i]];  // ��sdp[j]
        }
    }

    // ��X�̲׵��G�Adp[k]��ܯ�զX�X���Bk���覡�ƶq
    printf("%d\n", dp[k]);

    return 0;
}
