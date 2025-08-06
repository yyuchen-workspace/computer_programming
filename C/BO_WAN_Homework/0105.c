#include <stdio.h>
#include <stdint.h>

// 函式用於將 16 位無符號整數轉換為二進位格式並印出
void printBinary(uint16_t hexValue) {
    for (int i = 15; i >= 0; i--) {
        printf("%d", (hexValue >> i) & 1);  // 提取每個位元並輸出
        if (i % 4 == 0) {  // 每 4 位增加一個空格，方便閱讀
            printf(" ");
        }
    }
    printf("\n");
}

// 轉換為有符號整數（Signed Integer）
int16_t toSignedInt(uint16_t hexValue) {
    // 判斷符號位是否為 1，如果為 1，表示負數，使用兩補數表示法
    if ((hexValue & 0x8000) != 0) {  // 檢查最高位（符號位）
        return (int16_t)(hexValue - 0x10000);  // 兩補數轉換
    }
    return (int16_t)hexValue;  // 正數直接轉換
}

// 轉換為浮點數（Float）
void toFloat(uint16_t hexValue) {
    int sign = (hexValue >> 15) & 1;  // 符號位（S）
    int exponent = (hexValue >> 10) & 0x1F;  // 指數位（5 位）
    int fraction = hexValue & 0x3FF;  // 小數位（10 位）

    // 轉換成浮點數的科學記號表示法 S(1.F) * 2^(EXP - 15)
    double mantissa = 1.0;
    for (int i = 0; i < 10; i++) {
        if ((fraction >> (9 - i)) & 1) {
            mantissa += 1.0 / (1 << (i + 1));
        }
    }

    int actualExponent = exponent - 15;
    if (sign == 1) {
        mantissa = -mantissa;
    }

    // 輸出為科學記號表示法
    printf("Converted float is: %.6f*2^%d\n", mantissa, actualExponent);
}

int main() {
    uint16_t hexValue;
    int outputType;

    // 讀取十六進位數字
    printf("Please input a hex: ");
    scanf("%x", &hexValue);

    // 讀取使用者選擇的輸出類型
    printf("Please choose the output type(1:integer ,2:unsigned integer ,3:float):");
    scanf("%d", &outputType);

    // 輸出二進位格式
    printf("Binary of %X is: ", hexValue);
    printBinary(hexValue);

    // 根據選擇的類型進行相應的轉換
    switch (outputType) {
        case 1:  // 有符號整數（Signed Integer）
            printf("Converted signed integer is: %d\n", toSignedInt(hexValue));
            break;
        case 2:  // 無符號整數（Unsigned Integer）
            printf("Converted unsigned integer is: %u\n", hexValue);
            break;
        case 3:  // 浮點數（Float）
            toFloat(hexValue);
            break;
        default:
            printf("Invalid output type.\n");
            break;
    }

    return 0;
}
