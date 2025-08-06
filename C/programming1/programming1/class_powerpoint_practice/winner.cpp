#include<stdio.h>
int main()
{
    int scores[5] = {};
    int *p = &scores[0];
    *(p+1) = 100;
    p += 2;
    *p = 200;

    for (int i=0; i<5; i+=1)
    {
        printf("%d ", scores[i]);
    }
    printf("\nDifference: %d", &scores[3] - &scores[1]);
}
