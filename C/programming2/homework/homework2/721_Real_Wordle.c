#include <stdio.h>
#include <stdbool.h>

int main() {
    char guess[6], answer[6], result[6];
    scanf("%s %s", guess, answer);

    bool used_in_answer[5] = { false };  // 標記謎底中哪些字母被使用過
    bool used_in_guess[5] = { false };   // 標記猜測中哪些字母已被處理
    int i, j;

    // 第一次遍歷，處理綠色字母
    for (i = 0; i < 5; i++) {
        if (guess[i] == answer[i]) {
            result[i] = 'G';
            used_in_guess[i] = true;
            used_in_answer[i] = true;
        }
    }

    // 第二次遍歷，處理黃色字母
    for (i = 0; i < 5; i++) {
        if (result[i] != 'G') {  // 只有不是綠色的才檢查
            for (j = 0; j < 5; j++) {
                if (guess[i] == answer[j] && !used_in_answer[j] && !used_in_guess[i]) {
                    result[i] = 'Y';
                    used_in_answer[j] = true;
                    used_in_guess[i] = true; // 記錄已經處理的字母
                    break;
                }
            }
        }
    }

    // 第三次遍歷，處理白色字母
    for (i = 0; i < 5; i++) {
        if (result[i] != 'G' && result[i] != 'Y') {
            result[i] = '-';
        }
    }

    // 輸出結果
    for (i = 0; i < 5; i++) {
        printf("%c", result[i]);
    }
    printf("\n");

    return 0;
}
