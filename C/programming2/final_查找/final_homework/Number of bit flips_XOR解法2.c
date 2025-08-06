#include<stdio.h>

int main()
{

    int xor = a ^ b;
    while(xor)
    {
        count += xor & 1;
        xor >>= 1;
    }

}
