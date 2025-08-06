#include<stdio.h>

int gcd(int a, int b)
{
    if(a % b == 0)
    {
        return b;
    }
    else
    {
        gcd(b, a % b);
    }
}

int lcm(int a, int b)
{
    return (a * b) / gcd(a, b);
}

int main()
{
    int A, B;
    scanf("%d%d", &A, &B);
    printf("%d", lcm(A, B));

    return 0;
}
