#include<stdio.h>
#include<stdbool.h>
int main()
{
    int times = 0, num[20][10];
    scanf("%d", &times);
    for(int i = 0 ; i < times ; i++)
    {
            for(int j = 0 ; j < 10 ; j++)
            {
                scanf("%d", &num[i][j]);
            }
    }
    printf("Lumberjacks:\n");
    for(int i = 0 ; i < times ; i++)
    {
        bool ordered = true;
        int start = 0;

        while(num[i][start] == num[i][start + 1])//如果重複則迴圈到不重複
        {
            start+=1;
        }

        if(num[i][start] > num[i][start + 1])
        {
            for(int j = start + 1 ; j < 9 ; j++)
            {
                if(num[i][j] < num[i][j+1])
                {
                    ordered = false;
                    printf("Unordered\n");
                    break;
                }
            }
        }
        else if(num[i][start] < num[i][start + 1])
        {
            for(int j = start + 1 ; j < 9 ; j++)
            {
                if(num[i][j] > num[i][j+1])
                {
                    ordered = false;
                    printf("Unordered\n");
                    break;
                }
            }
        }

        if(ordered)
        {
            printf("Ordered\n");
        }
    }
    return 0;
}
