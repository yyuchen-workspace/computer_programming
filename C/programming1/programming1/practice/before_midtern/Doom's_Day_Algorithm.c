#include<stdio.h>
int main()
{
    //2011/1/1是星期六
    int times;
    int month_days[] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    scanf("%d", &times);
    for(int i = 0 ; i < times ; i++)
    {
        int M, D;
        scanf("%d %d", &M, &D);
        int days = 0;
        days = month_days[M - 1];
        days = days + D - 1;
        days %= 7;
        switch(days)
        {
            case 0:
                printf("Saturday\n");
                break;
            case 1:
                printf("Sunday\n");
                break;
            case 2:
                printf("Monday\n");
                break;
            case 3:
                printf("Tuesday\n");
                break;
            case 4:
                printf("Wednesday\n");
                break;
            case 5:
                printf("Thursday\n");
                break;
            case 6:
                printf("Friday\n");
                break;
        }
    }
    return 0;
}
