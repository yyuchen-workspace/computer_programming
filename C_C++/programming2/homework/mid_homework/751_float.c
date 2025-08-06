#include<stdio.h>

int main()
{
    float f;
    scanf("%f", &f);
    int i;
    i = *((int *) &f);
    i = (i >> 23) & 0xFF;  // 右移23位後，取出高 8 位
    printf("%d", i);
}
