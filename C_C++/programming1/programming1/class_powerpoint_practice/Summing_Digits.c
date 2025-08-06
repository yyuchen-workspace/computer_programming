#include<stdio.h>
int main()
{
    int num = 0;
    int sum = 0;
    scanf("%d", &num);
    while(num != 0)
    {
        while(num >= 10)
        {
            int sum = 0;
            while(num > 0)
            {
                sum += num % 10;
                num /= 10;
            }
            num = sum;

        }

        printf("%d\n", num);
        scanf("%d", &num);
    }

    return 0;
}
