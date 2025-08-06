#include <stdio.h>
#include <stdlib.h>

/**
 * 遞迴練習 - 包含多個經典遞迴問題
 * 每個函數都使用遞迴方法實作
 */

// ======================== 1. 階乘計算 ========================

/**
 * 計算 n 的階乘 (n!)
 * 遞迴定義: n! = n * (n-1)!, 且 0! = 1
 * 
 * @param n 非負整數
 * @return n 的階乘
 */
long long factorial(int n) {
    // 基礎情況: 0! = 1, 1! = 1
    if (n <= 1) {
        return 1;
    }
    
    // 遞迴情況: n! = n * (n-1)!
    return n * factorial(n - 1);
}

// ======================== 2. 費波那契數列 ========================

/**
 * 計算費波那契數列第 n 項
 * 遞迴定義: F(n) = F(n-1) + F(n-2), 且 F(0) = 0, F(1) = 1
 * 
 * @param n 項數
 * @return 第 n 項費波那契數
 */
long long fibonacci(int n) {
    // 基礎情況
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    // 遞迴情況: F(n) = F(n-1) + F(n-2)
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// ======================== 3. 最大公約數 (GCD) ========================

/**
 * 使用歐幾里得演算法計算最大公約數
 * 遞迴定義: gcd(a, b) = gcd(b, a % b), 且 gcd(a, 0) = a
 * 
 * @param a 第一個數
 * @param b 第二個數
 * @return a 和 b 的最大公約數
 */
int gcd(int a, int b) {
    // 基礎情況: 當 b = 0 時，最大公約數為 a
    if (b == 0) {
        return a;
    }
    
    // 遞迴情況: gcd(a, b) = gcd(b, a % b)
    return gcd(b, a % b);
}

// ======================== 4. 數字反轉 ========================

/**
 * 遞迴反轉一個整數
 * 
 * @param n 要反轉的數字
 * @param reversed 目前已反轉的部分
 * @return 反轉後的數字
 */
int reverse_number(int n, int reversed) {
    // 基礎情況: 數字為 0 時，返回已反轉的結果
    if (n == 0) {
        return reversed;
    }
    
    // 遞迴情況: 取出最後一位數字，加入到反轉結果中
    return reverse_number(n / 10, reversed * 10 + n % 10);
}

// ======================== 5. 十進制轉二進制 ========================

/**
 * 遞迴將十進制數轉換為二進制（以字串形式打印）
 * 
 * @param n 十進制數
 */
void decimal_to_binary(int n) {
    // 基礎情況: 數字為 0 或 1 時直接打印
    if (n <= 1) {
        printf("%d", n);
        return;
    }
    
    // 遞迴情況: 先處理較高位，再處理當前位
    decimal_to_binary(n / 2);
    printf("%d", n % 2);
}

// ======================== 6. 數字位數計算 ========================

/**
 * 遞迴計算一個正整數的位數
 * 
 * @param n 正整數
 * @return 位數
 */
int count_digits(int n) {
    // 基礎情況: 單位數
    if (n < 10) {
        return 1;
    }
    
    // 遞迴情況: 位數 = 1 + 去掉最後一位數字後的位數
    return 1 + count_digits(n / 10);
}

// ======================== 7. 數字各位數總和 ========================

/**
 * 遞迴計算一個數字各位數的總和
 * 
 * @param n 數字
 * @return 各位數總和
 */
int sum_of_digits(int n) {
    // 基礎情況: 單位數
    if (n < 10) {
        return n;
    }
    
    // 遞迴情況: 總和 = 最後一位 + 其餘位數的總和
    return (n % 10) + sum_of_digits(n / 10);
}

// ======================== 輔助函數 ========================

/**
 * 打印分隔線
 */
void print_separator() {
    printf("================================\n");
}

/**
 * 打印菜單
 */
void print_menu() {
    printf("\n=== 遞迴練習選單 ===\n");
    printf("1. 階乘計算 (n!)\n");
    printf("2. 費波那契數列\n");
    printf("3. 最大公約數 (GCD)\n");
    printf("4. 數字反轉\n");
    printf("5. 十進制轉二進制\n");
    printf("6. 計算數字位數\n");
    printf("7. 數字各位數總和\n");
    printf("0. 結束程式\n");
    printf("==================\n");
    printf("請選擇功能 (0-7): ");
}

// ======================== 主程式 ========================

int main() {
    int choice;
    int num1, num2;
    
    printf("歡迎使用遞迴練習程式！\n");
    printf("本程式包含多個經典遞迴問題的實作\n");
    
    while (1) {
        print_menu();
        
        if (scanf("%d", &choice) != 1) {
            printf("輸入錯誤，請輸入數字！\n");
            while (getchar() != '\n'); // 清空輸入緩存
            continue;
        }
        
        print_separator();
        
        switch (choice) {
            case 1:
                printf("階乘計算\n");
                printf("請輸入一個非負整數: ");
                scanf("%d", &num1);
                
                if (num1 < 0) {
                    printf("錯誤：階乘不支援負數！\n");
                } else if (num1 > 20) {
                    printf("警告：數字過大，結果可能溢出！\n");
                    printf("%d! = %lld\n", num1, factorial(num1));
                } else {
                    printf("%d! = %lld\n", num1, factorial(num1));
                }
                break;
                
            case 2:
                printf("費波那契數列\n");
                printf("請輸入項數 n (建議 n < 40): ");
                scanf("%d", &num1);
                
                if (num1 < 0) {
                    printf("錯誤：項數必須為非負整數！\n");
                } else if (num1 > 40) {
                    printf("警告：計算時間可能很長！\n");
                    printf("F(%d) = %lld\n", num1, fibonacci(num1));
                } else {
                    printf("F(%d) = %lld\n", num1, fibonacci(num1));
                }
                break;
                
            case 3:
                printf("最大公約數計算\n");
                printf("請輸入兩個正整數: ");
                scanf("%d %d", &num1, &num2);
                
                if (num1 <= 0 || num2 <= 0) {
                    printf("錯誤：請輸入正整數！\n");
                } else {
                    printf("gcd(%d, %d) = %d\n", num1, num2, gcd(num1, num2));
                }
                break;
                
            case 4:
                printf("數字反轉\n");
                printf("請輸入一個正整數: ");
                scanf("%d", &num1);
                
                if (num1 < 0) {
                    printf("錯誤：請輸入正整數！\n");
                } else {
                    printf("原數字: %d\n", num1);
                    printf("反轉後: %d\n", reverse_number(num1, 0));
                }
                break;
                
            case 5:
                printf("十進制轉二進制\n");
                printf("請輸入一個非負整數: ");
                scanf("%d", &num1);
                
                if (num1 < 0) {
                    printf("錯誤：請輸入非負整數！\n");
                } else {
                    printf("十進制: %d\n", num1);
                    printf("二進制: ");
                    decimal_to_binary(num1);
                    printf("\n");
                }
                break;
                
            case 6:
                printf("計算數字位數\n");
                printf("請輸入一個正整數: ");
                scanf("%d", &num1);
                
                if (num1 <= 0) {
                    printf("錯誤：請輸入正整數！\n");
                } else {
                    printf("數字 %d 有 %d 位\n", num1, count_digits(num1));
                }
                break;
                
            case 7:
                printf("數字各位數總和\n");
                printf("請輸入一個非負整數: ");
                scanf("%d", &num1);
                
                if (num1 < 0) {
                    printf("錯誤：請輸入非負整數！\n");
                } else {
                    printf("數字 %d 的各位數總和 = %d\n", num1, sum_of_digits(num1));
                }
                break;
                
            case 0:
                printf("感謝使用遞迴練習程式！再見！\n");
                return 0;
                
            default:
                printf("錯誤：請選擇 0-7 之間的數字！\n");
                break;
        }
        
        print_separator();
        printf("按 Enter 鍵繼續...");
        while (getchar() != '\n'); // 清空輸入緩存
        getchar(); // 等待用戶按 Enter
    }
    
    return 0;
}

/*
 * 編譯和執行:
 * gcc -o recursion_practice recursion_practice.c
 * ./recursion_practice
 * 
 * 每個遞迴函數的特點:
 * 1. 階乘: 經典遞迴，時間複雜度 O(n)
 * 2. 費波那契: 指數時間複雜度 O(2^n)，效率較低
 * 3. GCD: 歐幾里得演算法，時間複雜度 O(log min(a,b))
 * 4. 數字反轉: 線性遞迴，時間複雜度 O(log n)
 * 5. 進制轉換: 線性遞迴，時間複雜度 O(log n)
 * 6. 位數計算: 線性遞迴，時間複雜度 O(log n)
 * 7. 位數總和: 線性遞迴，時間複雜度 O(log n)
 */