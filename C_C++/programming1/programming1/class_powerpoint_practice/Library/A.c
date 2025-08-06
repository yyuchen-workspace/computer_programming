#include<stdio.h>
#include<stdbool.h>
int main()
{
    int times;
    scanf("%d", &times);
    for(int i = 0 ; i < times ; i++)
    {
        int number = 0, sum[1000] = {0}, answer = 0;
        int a = 0;
        scanf("%d", &number);
        for(int j = 1 ; j < number / 2 + 1; j++)
        {
            bool end = false;
            for(int k = 0 ; k < a ; k++)
            {
                if(j == sum[k])
                {
                    end = true;
                    break;
                }
            }
            for(int k = 0 ; k < number / 2 + 1; k++)
            {

                if(end)
                {
                    break;
                }
                else if(j * k == number)
                {
                    if(j == k)
                    {
                        sum[a]= j;
                        a+=1;
                    }
                    else
                    {
                        sum[a]= j;
                        sum[a + 1]= k;
                        a += 2;
                    }
                }
            }
        }
        answer += 1;
        for(int j = 0 ; j < a ; j++)
        {

                printf("%d ", sum[j]);
                answer += sum[j];


        }
        printf("%d ", answer);

        if(answer < number)
        {
            printf("deficient\n");
        }
        else if(answer == number)
        {
            printf("perfect\n");
        }
        else
        {
            printf("abundant\n");
        }
    }
    return 0;
}
