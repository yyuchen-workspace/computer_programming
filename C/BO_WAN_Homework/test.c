#include <stdio.h>

int main() {
    int num = 10;
    int *s = &num;
    printf("s is %p\n", s);
    printf("&s = %p\n", &s);
    printf("*s = %d\n", *s);
    return 0;
}
