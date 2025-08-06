#include <stdio.h>
#include <stdlib.h>

/**
 * 河內塔遞迴求解函數
 * 
 * @param n 圓盤數量
 * @param source 起始柱的名稱
 * @param destination 目標柱的名稱  
 * @param auxiliary 輔助柱的名稱
 * @param step_count 步驟計數器的指針，用於記錄總移動次數
 */
void hanoi(int n, char source, char destination, char auxiliary, int *step_count) {
    // 基礎情況：只有一個圓盤時，直接移動
    if (n == 1) {
        (*step_count)++;
        printf("步驟 %d: 移動圓盤 %d 從 %c 到 %c\n", *step_count, n, source, destination);
        return;
    }
    
    // 遞迴情況：n > 1
    // 步驟1: 將上面的 n-1 個圓盤從起始柱移到輔助柱（使用目標柱作為暫時輔助）
    hanoi(n-1, source, auxiliary, destination, step_count);
    
    // 步驟2: 將最底下的大圓盤從起始柱移到目標柱
    (*step_count)++;
    printf("步驟 %d: 移動圓盤 %d 從 %c 到 %c\n", *step_count, n, source, destination);
    
    // 步驟3: 將 n-1 個圓盤從輔助柱移到目標柱（使用起始柱作為暫時輔助）
    hanoi(n-1, auxiliary, destination, source, step_count);
}

/**
 * 計算河內塔最小移動次數的數學公式
 * 
 * @param n 圓盤數量
 * @return 最小移動次數 (2^n - 1)
 */
long long calculate_min_moves(int n) {
    // 使用位運算計算 2^n - 1
    return (1LL << n) - 1;
}

/**
 * 驗證輸入的有效性
 * 
 * @param n 圓盤數量
 * @return 1 表示有效，0 表示無效
 */
int validate_input(int n) {
    if (n < 1) {
        printf("錯誤：圓盤數量必須大於 0\n");
        return 0;
    }
    if (n > 20) {
        printf("警告：圓盤數量過大 (%d)，移動次數將會非常多 (2^%d - 1 = %lld 次)\n", 
               n, n, calculate_min_moves(n));
        printf("是否繼續？(y/n): ");
        char choice;
        scanf(" %c", &choice);
        if (choice != 'y' && choice != 'Y') {
            return 0;
        }
    }
    return 1;
}

/**
 * 顯示河內塔問題的介紹
 */
void print_introduction() {
    printf("=== 河內塔問題求解程式 ===\n");
    printf("規則：\n");
    printf("1. 有三根柱子：A(起始), B(輔助), C(目標)\n");
    printf("2. 起始柱上有 n 個圓盤，大盤在下，小盤在上\n");
    printf("3. 目標：將所有圓盤移到目標柱\n");
    printf("4. 限制：每次只能移動一個圓盤，大盤不能放在小盤上\n");
    printf("=============================\n\n");
}

/**
 * 顯示求解結果的統計資訊
 * 
 * @param n 圓盤數量
 * @param actual_moves 實際移動次數
 */
void print_statistics(int n, int actual_moves) {
    long long theoretical_moves = calculate_min_moves(n);
    
    printf("\n=== 求解完成 ===\n");
    printf("圓盤數量: %d\n", n);
    printf("實際移動次數: %d\n", actual_moves);
    printf("理論最小次數: %lld\n", theoretical_moves);
    printf("是否達到最優解: %s\n", (actual_moves == theoretical_moves) ? "是" : "否");
    printf("==============\n");
}

int main() {
    int n;              // 圓盤數量
    int step_count = 0; // 步驟計數器
    
    // 顯示程式介紹
    print_introduction();
    
    // 輸入圓盤數量
    printf("請輸入圓盤數量: ");
    if (scanf("%d", &n) != 1) {
        printf("錯誤：請輸入有效的整數\n");
        return 1;
    }
    
    // 驗證輸入
    if (!validate_input(n)) {
        printf("程式結束\n");
        return 1;
    }
    
    // 顯示問題資訊
    printf("\n開始求解 %d 個圓盤的河內塔問題...\n", n);
    printf("理論最小移動次數: %lld\n\n", calculate_min_moves(n));
    
    // 求解河內塔問題
    // 從柱子A移動到柱子C，使用柱子B作為輔助
    hanoi(n, 'A', 'C', 'B', &step_count);
    
    // 顯示統計資訊
    print_statistics(n, step_count);
    
    return 0;
}

/*
 * 編譯和執行方法:
 * 
 * 編譯: gcc -o hanoi hanoi.c
 * 執行: ./hanoi
 * 
 * 程式說明:
 * 1. 使用遞迴方法求解河內塔問題
 * 2. 支援輸入驗證和錯誤處理
 * 3. 顯示詳細的移動步驟
 * 4. 提供統計資訊和最優性驗證
 * 5. 對於大數量圓盤提供警告
 * 
 * 範例輸出 (n=3):
 * 步驟 1: 移動圓盤 1 從 A 到 C
 * 步驟 2: 移動圓盤 2 從 A 到 B  
 * 步驟 3: 移動圓盤 1 從 C 到 B
 * 步驟 4: 移動圓盤 3 從 A 到 C
 * 步驟 5: 移動圓盤 1 從 B 到 A
 * 步驟 6: 移動圓盤 2 從 B 到 C
 * 步驟 7: 移動圓盤 1 從 A 到 C
 */