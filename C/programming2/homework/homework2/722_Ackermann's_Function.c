#include<stdio.h>

int Ackerman(int a, int b)
{
    if(a == 0)
    {
        return b+=1;
    }
    else if(a > 0 && b == 0)
    {
        return Ackerman(a-1, 1);
    }
    else if(a > 0 && b > 0)
    {
        return Ackerman(a - 1, Ackerman(a, b - 1));
    }
}


int main()
{
    int m, n;
    scanf("%d%d", &m, &n);
    printf("%d", Ackerman(m, n));

    return 0;
}
