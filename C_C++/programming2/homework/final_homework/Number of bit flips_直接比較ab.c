
#include<stdio.h>

int main()
{
    int a, b;
    int count = 0;
    scanf("%d%d", &a, &b);
    for(int i = 0 ; i < 14 ; i++)
    {
        int bit_a = a >> i & 1;
        int bit_b = b >> i & 1;
        if(bit_a != bit_b)
        {
            count+=1;
        }
    }

    printf("%d\n", count);
}
