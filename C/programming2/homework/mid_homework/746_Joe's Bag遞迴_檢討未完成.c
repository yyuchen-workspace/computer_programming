#include <stdio.h>

int countCombinations(int coins[], int n, int k, int index) {
    // �򥻱��p�G��ؼЪ��B��0�A��ܧ��@�ӲզX
    if (k == 0) {
        return 1;
    }

    // �򥻱��p�G��ؼЪ��B�p��0�ΨS����h�U�l�i��A��ܳo�����|�L��
    if (k < 0 || index == n) {
        return 0;
    }

    // ��ܷ�e�U�l�A���~�򻼰j
    int includeCurrent = countCombinations(coins, n, k - coins[index], index + 1);

    // ����ܷ�e�U�l�A���~�򻼰j
    int excludeCurrent = countCombinations(coins, n, k, index + 1);

    // ��^��ܩΤ���ܪ����G���M
    return includeCurrent + excludeCurrent;
}

int main() {
    int n, k;
    scanf("%d", &n);  // Ū���U�l���ƶq
    int coins[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &coins[i]);  // Ū���C�ӳU�l�������B
    }
    scanf("%d", &k);  // Ū�����O��������

    // �q��0�ӳU�l�}�l���j�A�ôM��Ҧ��i�઺�զX
    int result = countCombinations(coins, n, k, 0);

    // ��X���G
    printf("%d\n", result);

    return 0;
}

