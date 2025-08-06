#include <stdio.h>
#include <stdlib.h>

int main() {
    const char *binary_string = "1101"; // 這是二進制字串
    int num;

    // 使用 strtol 將二進制字串轉換為整數
    num = (int)strtol(binary_string, NULL, 2); // '2' 表示我們提供的是二進制格式

    printf("二進制：%s\n", binary_string);
    printf("對應的整數：%d\n", num);

    return 0;
}
