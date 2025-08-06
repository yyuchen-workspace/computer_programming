#include<stdio.h>
#include<string.h>
#include<stdint.h>

int main() {
    uint32_t n1, n2, sum;
    printf("Please enter the first number: ");
    scanf("%u", &n1);
    printf("Please enter the second number: ");
    scanf("%u", &n2);

    int array1[10] = {0}, array2[10] = {0}, array_sum[20] = {0};
    int total1 = 0, total2 = 0, total_sum = 0;

    sum = n1 * n2;

    // 将n1和n2分解成各个位的数字
    while(n1 > 0) {
        array1[total1++] = n1 % 10;
        n1 /= 10;
    }

    while(n2 > 0) {
        array2[total2++] = n2 % 10;
        n2 /= 10;
    }

    // 打印第一行数字 n1
    for (int i = total1 - 1; i >= 0; i--) {
        printf("%d ", array1[i]);
    }
    printf("\n");

    // 打印乘号和第二行数字 n2
    printf("*) ");
    for (int i = total2 - 1; i >= 0; i--) {
        printf("%d ", array2[i]);
    }
    printf("\n");

    // 计算并打印部分积
    int distribute[10][20] = {0};
    for (int i = 0; i < total2; i++) {
        int carry = 0;
        for (int j = 0; j < total1; j++) {
            int product = array2[i] * array1[j] + carry;
            distribute[i][i + j] = product % 10;
            carry = product / 10;
        }
        distribute[i][i + total1] = carry; // 存储进位

        // 打印部分积
        for (int k = total1 - i; k >= 0; k--)
        {
            printf("  "); // 打印前导空格
        }
        for (int j = total1; j >= 0; j--) {
            if(distribute[i][i + j] == 0)
            {
                printf(" ");
            }
            else 
            {
                printf("%d ", distribute[i][i + j]);
            }
        }
        printf("\n");
    }

    // 将部分积相加
    for (int i = 0; i < total1 + total2; i++) {
        int sum_col = 0;
        for (int j = 0; j < total2; j++) {
            sum_col += distribute[j][i];
        }
        array_sum[i] += sum_col;
        if (array_sum[i] >= 10) {
            array_sum[i + 1] += array_sum[i] / 10;
            array_sum[i] %= 10;
        }
    }

    // 打印分隔线
    for (int i = 0; i < total1 + total2; i++) {
        printf("--");
    }
    printf("\n");

    // 打印最终乘积结果
    int start_print = 0;
    for (int i = total1 + total2; i >= 0; i--) {
        if (array_sum[i] != 0) {
            start_print = 1;
        }
        if (start_print) {
            printf("%d ", array_sum[i]);
        }
    }
    printf("\n");

    return 0;
}
