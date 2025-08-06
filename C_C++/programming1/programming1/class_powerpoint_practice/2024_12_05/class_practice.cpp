#include<stdio.h>
#include<string.h>
constexpr int row = 2;
constexpr int column = 10;


int main()
{
    char ch[column] = {0};
    for(int i = 0 ; i < row ; i++)
    {
        fgets(ch, sizeof(ch), stdin);
        printf("Input is [%s].\n", ch);
    }
    /*
    char ch[row][column] = {0};
    for(int i = 0 ; i < row ; i++)
    {
        fgets(ch[i], sizeof(ch[i]), stdin);
        ch[i][strcspn(ch[i], "\n")] = '\0';
        for(int i = 0 ; i < sizeof(ch) / sizeof(ch[i]) ; i++)
        {
            if(ch[i][])
        }

        printf("Input is [%s].\n", ch[i]);
    }
    */
    /*
    char ch[column] = {0};
    int count = 0;
    for(int i = 0 ; i < column ; i++)
    {
        ch[i] = getchar();
    }
    for(int i = 0 ; i < column ; i++)
    {
        printf("%c", ch[i]);
    }
    */



    /*
    char ch;
    getchar()
    */

/*
    char ch[row][column] = {0};
    for(int i = 0 ; i < row ; i++)
    {
        fgets(ch[i], sizeof(ch[i]), stdin);
        ch[i][strcspn(ch[i], "\n")] = '\0';
        printf("Input is [%s].\n", ch);
    }
    */
}
