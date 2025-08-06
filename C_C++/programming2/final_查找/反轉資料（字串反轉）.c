#include <stdio.h>
#include <string.h>

#define MAX 100
char stack[MAX];
int top = -1;

void reverse(char* str) {
    for (int i = 0; str[i]; i++)
        stack[++top] = str[i];

    for (int i = 0; str[i]; i++)
        str[i] = stack[top--];
}

int main() {
    char str[] = "abcdefg";
    reverse(str);
    printf("¤ÏÂà«á: %s\n", str);
    return 0;
}

