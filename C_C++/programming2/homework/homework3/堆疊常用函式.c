#include <stdio.h>
#include <string.h>

#define MAX 100

typedef struct {
    char data[MAX];
    int top;
} Stack;

void init(Stack* s) {
    s->top = -1;
}

int is_full(Stack* s) {
    return s->top == MAX - 1;
}

int is_empty(Stack* s) {
    return s->top == -1;
}

int push(Stack* s, char ch) {
    if (is_full(s)) return 0;
    s->data[++(s->top)] = ch;
    return 1;
}

char pop(Stack* s) {
    if (is_empty(s)) return '\0';
    return s->data[(s->top)--];
}
