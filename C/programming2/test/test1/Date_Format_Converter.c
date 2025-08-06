#include<stdio.h>
#include<string.h>
#include<ctype.h>

int main()
{
    char input[101] = {};
    scanf("%s", input);
    int output[8] = {};
    int num = 0;
    for(int i = 0, sz = strlen(input); i < sz ; i++)
    {

        if(isdigit(input[i]))
        {
            output[num] = input[i] - '0';
            num++;
        }




    }

    for(int i = 0 ; i < 8 ; i++)
    {
        printf("%d", output[i]);

    }

}

