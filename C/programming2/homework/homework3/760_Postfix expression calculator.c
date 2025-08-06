#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_SIZE 100

int main() {
    int n;
    char expn[105]; // �̦h 100 �Ӧr�� + '\0'

    scanf("%d %s", &n, expn);

    int stack[MAX_SIZE];
    int top = -1;

    for (int i = 0; i < n; i++) {
        char ch = expn[i];

        if (isdigit(ch)) {
            // �p�G�O�Ʀr�A�ন int �� push
            stack[++top] = ch - '0';
        } else {
            // �O�B��l�Apop ��ӼƦr
            int b = stack[top--];
            int a = stack[top--];
            int result;

            switch (ch) {
                case '+': result = a + b; break;
                case '-': result = a - b; break;
                case '*': result = a * b; break;
                case '/': result = a / b; break; // �D�ثO�Ҿ�ư��k�A�L�ݳB�z���H 0
            }

            stack[++top] = result;
        }
    }

    printf("%d\n", stack[top]);
    return 0;
}
