#include<stdio.h>
int main()
{
    int table[5][4] = {0}, height = 0, weight = 0;
    printf("Please input your height and weight (0 0 to stop and display the statistics)...>\n");
    scanf("%d%d", &height, &weight);
    while(height != 0 || weight != 0)
    {
        if(weight >= 41 && weight <= 90 && height >= 151 && height <= 190)
        {
            table[(weight - 1) / 10 - 4][(height - 1) / 10 - 15] += 1;
        }
        scanf("%d%d", &height, &weight);
    }
    printf("-------------------------------\n");
    printf("           151~160 161~170 171~180 181~190\n");
    int scope;
    for(int i = 0 ; i < 5 ; i++)
    {
        scope = (i + 4) * 10 + 1;
        printf("%d ~ %d", scope, scope + 9);
        for(int j = 0 ; j < 4 ; j++)
        {
            printf("       %d", table[i][j]);
        }
        printf("\n");
    }
    return 0;
}
