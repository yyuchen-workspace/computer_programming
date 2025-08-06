#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    int N;
    char pattern[101], str[601];

    // ��J���
    scanf("%d", &N);
    scanf("%s", pattern);
    scanf("%s", str);

    // ����str������r�}�C
    char *words[100];
    int wordCount = 0;
    char *token = strtok(str, "|");

    while (token != NULL) {
        words[wordCount++] = token;
        token = strtok(NULL, "|");
    }

    // �ˬd�r�ƬO�_�@�P
    if (wordCount != N) {
        printf("false\n");
        return 0;
    }

    // �ϥΨ�Ӧr��Ӷi��ǰt
    char *patternToWord[26] = {NULL};  // 'a'��'z'������
    char *wordToPattern[100] = {NULL}; // ��r��pattern������

    for (int i = 0; i < N; i++) {
        int pIndex = pattern[i] - 'a';  // pattern���r������������
        char *currentWord = words[i];    // ��������r

        // �ˬd�r�����r���M�g
        if (patternToWord[pIndex] == NULL) {
            patternToWord[pIndex] = currentWord;  // �s���M�g
        } else if (strcmp(patternToWord[pIndex], currentWord) != 0) {
            printf("false\n");
            return 0;
        }

        // �ˬd��r��r�����M�g
        int wordIndex = i;  // �ϥί��ިӧ@����r��ID
        if (wordToPattern[wordIndex] == NULL) {
            wordToPattern[wordIndex] = &pattern[i];  // �s���M�g
        } else if (*wordToPattern[wordIndex] != pattern[i]) {
            printf("false\n");
            return 0;
        }
    }

    // �p�G�S���Ĭ�A�h�ǰt���\
    printf("true\n");

    return 0;
}
\
