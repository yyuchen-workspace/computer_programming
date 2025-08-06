#include <stdio.h>
#include <string.h>

int binary_to_int(const char *binary_string) {
    int num = 0;
    int length = strlen(binary_string);

    // 遍歷字串，計算每一位的值
    for (int i = 0; i < length; i++) {
        num = num * 2 + (binary_string[i] - '0');
    }

    return num;
}

int main() {
    const char *binary_string = "1101"; // 二進制字串
    int num;

    num = binary_to_int(binary_string); // 手動轉換為整數

    printf("二進制：%s\n", binary_string);
    printf("對應的整數：%d\n", num);

    return 0;
}

