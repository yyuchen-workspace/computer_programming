#include<stdio.h>

int main()
{
    int cases, month, day, date;//2011 Sunday
    int days[] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    scanf("%d", &cases);
    for(int i = 0 ; i < cases ; i++)
    {
        scanf("%d%d", &month, &day);
        int date = (days[month - 1] + day) % 7;
        switch(date){
        case 1: 
            printf("Saturday\n");
            break;
        case 2:
            printf("Sunday\n");
            break;
        case 3:
            printf("Monday\n");
            break;
        case 4:
            printf("Tuesday\n");
            break;
        case 5:
            printf("Wednesday\n");
            break;
        case 6:
            printf("Thursday\n");
            break;
        case 0:
            printf("Friday\n");
        }
    }

    return 0;
}