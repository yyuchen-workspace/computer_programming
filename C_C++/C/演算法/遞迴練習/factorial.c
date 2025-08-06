#include <stdio.h>

int factorial(int n)
{
    if (n <= 1)
        return 1;
    return n * factorial(n - 1);
}

int main()
{
    int n = 0;
    printf("請輸入一個非負整數: ");
    scanf("%d", &n);
    printf("階乘 %d! = %d\n", n, factorial(n));
    return 0;
}
