#include<stdio.h>
int main()
{
        char name[5][10] = {0};
        int score[5][4] = {0};
        for(int i = 0 ; i < 5; i++)
        {
            printf("Please enter student's name : ");
            scanf("%9s", name[i]);
            printf("Please enter three score : ");
            scanf("%d %d %d", &score[i][0], &score[i][1], &score[i][2]);
            score[i][3] = (score[i][0] + score[i][1] + score[i][2]) / 3;
            printf("Average for %s is %d \n", name[i], score[i][3]);
        }
        return 0;
}
