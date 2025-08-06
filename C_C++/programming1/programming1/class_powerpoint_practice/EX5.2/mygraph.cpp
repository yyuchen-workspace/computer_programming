#include<stdio.h>
#include<stdint.h>

void DrawLine(int32_t len)
{
    for(int i = 0 ; i < len ; i++)
    {
        printf("*");
    }
    printf("\n");


}


void DrawRectangle(int32_t row, int32_t col)
{

    for(int i = 0 ; i < row ; i++)
    {
       DrawLine(col);
    }
    printf("\n");
}


void DrawSquare(int32_t len)
{
    for(int i = 0 ; i < len ; i++)
    {
       DrawLine(len);
    }
    printf("\n");
}

