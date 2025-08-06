#include <stdio.h>

void print_binary(unsigned char num) {
    printf("二進制：");
    for (int i = 7; i >= 0; i--) {
        printf("%d", (num >> i) & 1);
    }
    printf("\n");
}

int main() {
    unsigned char value;

    printf("請輸入一個 0~255 的整數：");
    scanf("%hhu", &value);

    printf("十進制：%u\n", value);
    print_binary(value);

    return 0;
}
