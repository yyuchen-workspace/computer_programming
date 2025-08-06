#include<stdio.h>
int main()
{
    int times;
    scanf("%d", &times);
    for(int cases = 1 ; cases <= times ; cases++)
    {
        int a, b;
        int sum = 0;
        scanf("%d %d", &a, &b);
        if(a % 2 == 0)
        {
            a++;
        }
        for(int i = a ; i <= b ; i += 2)
        {
            sum += i;
        }
        printf("Case %d: %d\n", cases, sum);
    }
}
