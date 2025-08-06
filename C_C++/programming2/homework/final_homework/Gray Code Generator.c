#include<stdio.h>
#include<math.h>
int main()
{
    int n;
    scanf("%d", &n);

    int N = 1;
    for(int i = 0 ; i < n ; i++)
    {
        N*=2;
    }

    for(int i = 0 ; i < N ; i++)
    {
        int gray = 0;
        if(i == 0)
        {
            printf("0 ");
            continue;
        }
        if(i == 1)
        {
            printf("1 ");
            continue;
        }
        for(int j = n - 1; j >= 0 ; j--)
        {
            int pre;
            int cur = (i >> j) & 1;
            if(j == n - 1)
            {
                gray |= cur;
                gray <<= 1;
                pre = cur;
                continue;
            }

            int XOR = pre ^ cur;
            gray |= XOR;
            if(j == 0)
            {
                break;
            }
            gray <<= 1;

            pre = cur;
        }
        printf("%d ", gray);
    }
}
