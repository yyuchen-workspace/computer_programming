#include <stdio.h>
int main()
{
    char data[5]; // 增加一個空間來容納 null 結尾字符
    printf("請輸入五個字:");
    scanf_s("%s", &data, 5); // 指定最大可輸入的字符數為 5
    printf("您輸入的字為:%s\n", data);

    return 0;
}