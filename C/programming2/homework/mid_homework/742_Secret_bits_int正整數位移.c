#include<stdio.h>
#include<string.h>
#include<stdint.h>


int main()
{
    uint32_t n;
    scanf("%u", &n);
    n = n >> 4;
    printf("%d", n);
}
