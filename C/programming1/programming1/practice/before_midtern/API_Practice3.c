#include<stdio.h>
int main()
{
    int times, walls, wall1 = 0, wall2;

    scanf("%d", &times);
    for(int i = 1 ; i <= times ; i++)
    {
        int highjump = 0, lowjump = 0;
        scanf("%d", &walls);        
        scanf("%d", &wall1);
        
        for(int j = 1 ; j < walls ; j++)
        {
            scanf("%d", &wall2);
            if(wall2 > wall1)
            {
                highjump++;
            }   
            else if(wall2 < wall1)
            {
                lowjump++;
            }
            else
            {
                continue;
            }
            wall1 = wall2;
        }
            printf("Case %d: %d %d\n", i, highjump, lowjump);

    }
    return 0;
}