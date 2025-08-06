//使用堆疊檢查 (), {}, [] 是否對稱、正確閉合

#include <stdio.h>

#define MAX 100

char stack[MAX];
int top = -1;

int is_pair(char open, char close) {
    return (open == '(' && close == ')') ||
           (open == '[' && close == ']') ||
           (open == '{' && close == '}');
}

int is_balanced(const char* str) {
    for (int i = 0; str[i]; i++) {
        char ch = str[i];
        if (ch == '(' || ch == '[' || ch == '{') {
            stack[++top] = ch;
        } else if (ch == ')' || ch == ']' || ch == '}') {
            if (top == -1 || !is_pair(stack[top--], ch))
                return 0;
        }
    }
    return top == -1;
}

int main() {
    char expr[] = "{[(a+b)*c]+2}";
    if (is_balanced(expr))
        printf("括號配對正確\n");
    else
        printf("括號配對錯誤\n");
    return 0;
}
