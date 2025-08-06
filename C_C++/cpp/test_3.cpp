#include<stdio.h>
int main()
{
    int  d, g, r, dollar;
    int year = 0;
    printf("Please enter d g r");
    scanf("%d%d%d", &d, &g, &r);
    while(dollar < g)
    {
        dollar = (dollar + d) * (1 + r / 100.0);
        year++;
    }
    printf("We need %d year to reach the goal %d", year, g);

}