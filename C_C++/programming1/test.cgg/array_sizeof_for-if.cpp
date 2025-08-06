#include<stdio.h>
#include<string.h>

int main()
{
    char array[][10] =
    {
        "Hello C++",
        "LINE 2",
        "LINE 3"
    }; 
    int row = sizeof(array) / sizeof(char) / (sizeof(array[0])) / sizeof(char);
    //算有幾行
    //總字節/datatype/列數/datayype = 40/1/10/1 = 4
    int col = (sizeof(array[0])) / sizeof(char); //第一橫行字節數
    //printf("%d", row);
    for (int i = 0 ; i < row ; i++)
    {
        for(int j = 0 ; j < col ; j++)
        if(array[i] != 0)
        {
            printf("%c", array[i][j]);    
        }
        printf("\n");
    }

}
