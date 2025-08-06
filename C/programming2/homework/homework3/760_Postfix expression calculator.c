#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_SIZE 100

int main() {
    int n;
    char expn[105]; // 最多 100 個字元 + '\0'

    scanf("%d %s", &n, expn);

    int stack[MAX_SIZE];
    int top = -1;

    for (int i = 0; i < n; i++) {
        char ch = expn[i];

        if (isdigit(ch)) {
            // 如果是數字，轉成 int 並 push
            stack[++top] = ch - '0';
        } else {
            // 是運算子，pop 兩個數字
            int b = stack[top--];
            int a = stack[top--];
            int result;

            switch (ch) {
                case '+': result = a + b; break;
                case '-': result = a - b; break;
                case '*': result = a * b; break;
                case '/': result = a / b; break; // 題目保證整數除法，無需處理除以 0
            }

            stack[++top] = result;
        }
    }

    printf("%d\n", stack[top]);
    return 0;
}
