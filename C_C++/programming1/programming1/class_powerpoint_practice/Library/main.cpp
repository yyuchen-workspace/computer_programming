#include<stdio.h>
#include "header.h"

int cal_sum(int a, int b);

int main()
{
    int a = 10, b = 5, sum;
    sum = cal_sum(a, b);
    printf("%d", sum);

    return 0;
}
