#include <stdio.h>
#include <string.h>

void process(const char* src, char* result) {
    int top = 0;
    for (int i = 0; src[i] != '\0'; ++i) {
        if (src[i] == '#') {
            if (top > 0) top--; // backspace
        } else {
            result[top++] = src[i]; // push
        }
    }
    result[top] = '\0'; // µ²§ô¦r¦ê
}

int main() {
    char s[105], t[105];
    scanf("%s %s", s, t);

    char processedS[105], processedT[105];
    process(s, processedS);
    process(t, processedT);

    if (strcmp(processedS, processedT) == 0)
        printf("true\n");
    else
        printf("false\n");

    return 0;
}

/*
🔢 步驟分解
'1'	推入數字	[1]
'2'	推入數字	[1, 2]
'+'	1 + 2 = 3	[3]	彈出 2 和 1 相加，推入 3
'3'	推入數字	[3, 3]
'4'	推入數字	[3, 3, 4]
'+'	3 + 4 = 7	[3, 7]	彈出 4 和 3 相加，推入 7
'*'	3 × 7 = 21	[21]	彈出 7 和 3 相乘，推入 21
*/
