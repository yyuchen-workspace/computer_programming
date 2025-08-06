#include<stdio.h>

int main()
{
    int times, height, frequency;
    scanf("%d", &times);

    for(int i = 0 ; i < times ; i++)//幾次事件
    {
        scanf("%d%d", &height, &frequency);

        for(int j = 0 ; j < frequency ; j++)//幾個三角形
        {
            for(int k = 1 ; k <= height ; k++)//幾行
            {
                for(int l = k ; l > 0 ; l--)//長度
                {
                    printf("%d", k);
                }
                printf("\n");
            }

            for(int k = height - 1 ; k > 0 ; k--)//幾行
            {
                for(int l = k ; l > 0 ; l--)//長度
                {
                    printf("%d", k);
                }
                printf("\n");
            }
            if(j < frequency - 1)
            {
                printf("\n");
            }

        }

    }
    return 0;

}
