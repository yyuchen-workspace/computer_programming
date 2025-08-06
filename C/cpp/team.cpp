#include<stdio.h>
#include<stdbool.h>
#include"MyLibrary.h"

void team()
{
    int num;
    int a, b, c;
    int sum = 0;
    scanf("%d", &num);
    for(int i = 0 ; i < num ; i++)
    {
        scanf("%d%d%d", &a, &b, &c);
        if(a+b+c >= 2)
        {
            sum++;
        }
    }
    printf("%d", sum);

}

void sayhi()
{
    printf("Hi");
}



