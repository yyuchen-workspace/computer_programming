#include<stdio.h>

int main()
{
    int classification[10] = {0}, score;
    printf("Histogram\n\n");
    printf("Please input a score (-1 to stop and display the histogram)...>");
    scanf("%d", &score);

    while(score != -1)
    {
        if(score < 1)
        {
            classification[0] += 1;
        }
        else
        {
            classification[(score - 1) / 10] += 1;
        }
        scanf("%d", &score);
    }
    printf("-------------------------------\n");
    int range_start = 1;
    int range_end = 10;
    for(int i = 0 ; i < 10 ; i++)
    {
        if(i == 0)
        {
            printf(" 0~ 10 ");
        }
        else if(i == 9)
        {
            printf("91~100 ");
        }
        else
        {
            printf("%d~ %d ", range_start, range_end);
        }

        for(int j = 0 ; j < classification[i] ; j++)
        {
            printf("*");
        }
        printf("\n");

        range_start += 10;
        range_end += 10;

    }
    return 0;

}
