#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    int N;
    char pattern[101], str[601];

    // 輸入資料
    scanf("%d", &N);
    scanf("%s", pattern);
    scanf("%s", str);

    // 分割str成為單字陣列
    char *words[100];
    int wordCount = 0;
    char *token = strtok(str, "|");

    while (token != NULL) {
        words[wordCount++] = token;
        token = strtok(NULL, "|");
    }

    // 檢查字數是否一致
    if (wordCount != N) {
        printf("false\n");
        return 0;
    }

    // 使用兩個字典來進行匹配
    char *patternToWord[26] = {NULL};  // 'a'到'z'的對應
    char *wordToPattern[100] = {NULL}; // 單字到pattern的對應

    for (int i = 0; i < N; i++) {
        int pIndex = pattern[i] - 'a';  // pattern的字母對應的索引
        char *currentWord = words[i];    // 對應的單字

        // 檢查字母到單字的映射
        if (patternToWord[pIndex] == NULL) {
            patternToWord[pIndex] = currentWord;  // 新的映射
        } else if (strcmp(patternToWord[pIndex], currentWord) != 0) {
            printf("false\n");
            return 0;
        }

        // 檢查單字到字母的映射
        int wordIndex = i;  // 使用索引來作為單字的ID
        if (wordToPattern[wordIndex] == NULL) {
            wordToPattern[wordIndex] = &pattern[i];  // 新的映射
        } else if (*wordToPattern[wordIndex] != pattern[i]) {
            printf("false\n");
            return 0;
        }
    }

    // 如果沒有衝突，則匹配成功
    printf("true\n");

    return 0;
}
\
