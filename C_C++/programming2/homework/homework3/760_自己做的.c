#include <stdio.h>
#include <ctype.h>

#define MAX 100

int stack[MAX];
int top = -1;

void push(int x) {
    stack[++top] = x;
}

int pop() {
    return stack[top--];
}

int main() {
    int N;
    scanf("%d", &N);
    char exp[MAX];
    scanf("%s", exp);

    for (int i = 0; i < N; i++) {
        char ch = exp[i];
        if (isdigit(ch)) {
            push(ch - '0');
        } else {
            int b = pop();
            int a = pop();
            int result;
            switch (ch) {
                case '+': result = a + b; break;
                case '-': result = a - b; break;
                case '*': result = a * b; break;
                case '/': result = a / b; break;
            }
            push(result);
        }
    }

    printf("%d\n", pop());
    return 0;
}
