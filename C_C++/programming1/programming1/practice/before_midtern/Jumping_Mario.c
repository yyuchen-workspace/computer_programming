#include<stdio.h>
int main()
{
    int times;
    int height[50];
    scanf("%d", &times);
    for(int i = 0 ; i < times ; i++)
    {
        int walls = 0;
        int high_jumps = 0;
        int low_jumps = 0;
        scanf("%d", &walls);
        for(int j = 0 ; j < walls ; j++)
        {
            scanf("%d", &height[j]);
            if(j > 0 && height[j - 1] < height[j])
            {
                high_jumps++;
            }
            else if(j > 0 && height[j - 1] > height[j])
            {
                low_jumps++;
            }
            else
            {
                continue;
            }
        }

        printf("Case %d: %d %d\n", i + 1, high_jumps, low_jumps);


    }

    return 0;
}
