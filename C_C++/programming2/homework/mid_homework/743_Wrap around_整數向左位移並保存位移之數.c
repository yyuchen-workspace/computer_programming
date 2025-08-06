#include<stdio.h>
#include<stdint.h>

int main()
{
    uint32_t num;
    unsigned int n;
    scanf("%u%u", &num, &n);

    num = (num << n) | (num >> (32 - n));
    printf("%u", num);
}
