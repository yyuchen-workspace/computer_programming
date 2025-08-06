#include<stdio.h>

int main()
{
    int a, b;
    int count = 0;
    scanf("%d%d", &a, &b);
    int XOR = a ^ b;
    for(int i = 0 ; i < 14 ; i++)
    {
        if((XOR >> i & 1)!=0)
        {
            count+=1;
        }
    }
    printf("%d\n", count);
}
