#include<stdio.h>

int main()
{
int m = 0, n = 0, arr[3] = {1, 2 ,3};

int (*p2a)[3] = &arr; // p2a is int (*)[3]
(*p2a)[2] = m;
for(int i= 0 ; i < 3 ; i++)
{
    printf("%d ", (*p2a)[i]);
}
}

