#include <stdio.h>

char arr[7][3] = {"S0", "S1", "S2", "S3", "S4", "S5", "S6"}; // 定义状态数组
int results[7] = {0}; // 用来记录可能的状态

void while_loop(int num, int currentState);

int main() {
    int num;
    printf("Please enter an integer: ");
    scanf("%d", &num);

    while (num != 0) {
        while_loop(num, 0); // 从初始状态S0开始处理输入
        printf("Please enter an integer: ");
        scanf("%d", &num);
    }

    printf("Possible States: ");
    for (int i = 1; i < 7; i++) {
        if (results[i]) {
            printf("%s ", arr[i]);
        }
    }
    printf("\n");

    return 0;
}

void while_loop(int num, int currentState) {
    if (num == 0) return; // 输入结束

    switch (currentState) {
        case 0: // 初始状态 S0
            if (num % 2 != 0) { // 奇数
                results[1] = 1; // 可能状态 S1
                results[2] = 1; // 可能状态 S2
                while_loop(num, 1); // 继续处理S1
                while_loop(num, 2); // 继续处理S2
            } else { // 偶数
                results[3] = 1; // 可能状态 S3
                while_loop(num, 3); // 继续处理S3
            }
            break;

        case 1: // 状态 S1
            if (num % 2 != 0) { // 奇数
                results[3] = 1; // 可能状态 S3
                while_loop(num, 3); // 继续处理S3
            } else { // 偶数
                results[4] = 1; // 可能状态 S4
                results[5] = 1; // 可能状态 S5
                while_loop(num, 4); // 继续处理S4
                while_loop(num, 5); // 继续处理S5
            }
            break;

        case 2: // 状态 S2
            if (num % 2 != 0) { // 奇数
                results[4] = 1; // 可能状态 S4
                while_loop(num, 4); // 继续处理S4
            }
            break;

        case 3: // 状态 S3
            if (num % 2 != 0) { // 奇数
                results[4] = 1; // 可能状态 S4
                results[5] = 1; // 可能状态 S5
                while_loop(num, 4); // 继续处理S4
                while_loop(num, 5); // 继续处理S5
            }
            break;

        case 4: // 状态 S4
            break; // 没有进一步的转移

        case 5: // 状态 S5
            if (num % 2 != 0) { // 奇数
                results[6] = 1; // 可能状态 S6
            }
            break;

        case 6: // 状态 S6
            break; // 没有进一步的转移
    }
}
