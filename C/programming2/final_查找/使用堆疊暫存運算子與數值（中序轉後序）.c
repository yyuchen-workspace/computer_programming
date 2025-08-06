/*說明：
利用堆疊來暫存運算子

將中序表達式轉成後序（Postfix）再計算

🧩 範例輸入：3 + 4 * 2
*/

#include <stdio.h>
#include <ctype.h>

#define MAX 100

char stack[MAX];
int top = -1;

int precedence(char op) {
    if(op == '+' || op == '-') return 1;
    if(op == '*' || op == '/') return 2;
    return 0;
}

void push(char ch) {
    stack[++top] = ch;
}

char pop() {
    return stack[top--];
}

char peek() {
    return stack[top];
}

int is_empty() {
    return top == -1;
}

void infix_to_postfix(const char* expr) {
    for(int i = 0; expr[i]; i++) {
        char ch = expr[i];

        if(isdigit(ch)) {
            printf("%c ", ch);
        }
        else if(ch == '(') {
            push(ch);
        }
        else if(ch == ')') {
            while(!is_empty() && peek() != '(')
                printf("%c ", pop());
            pop(); // 移除 '('
        }
        else { // 運算子
            while(!is_empty() && precedence(peek()) >= precedence(ch))
                printf("%c ", pop());
            push(ch);
        }
    }
    while(!is_empty()) {
        printf("%c ", pop());
    }
}

int main() {
    char expr[] = "3+4*2";
    printf("後序表示: ");
    infix_to_postfix(expr);
    printf("\n");
    return 0;
}
