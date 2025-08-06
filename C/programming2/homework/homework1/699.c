#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<stdbool.h>

bool is_correct(const char *arr)
{
    bool correct = true;
    for(int i = 0 ; i < 5 ; i++)
    {
            if(!isalpha(arr[i]))
            {
                correct = false;
                break;
            }
            for(int j = 0 ; j < 5 ; j++)
            {
                if(i == j)
                {
                    continue;
                }
                if(arr[i] == arr[j])
                {
                    correct = false;
                    break;
                }
            }

    }

    return correct;
}


void up(char *arr)
{
    for(int i = 0 ; i < 5 ; i++)
    {
        if(islower(arr[i]))
        {
            arr[i] = toupper(arr[i]);
        }
    }
}


int main()
{
    char guess[6] = {};
    char answer[6] = {};

    scanf("%5s", guess);
    scanf("%5s", answer);

    bool correct = is_correct(guess);
    if(!correct)
    {
        printf("ERR\n");
        return 0;
    }
    is_correct(answer);
    if(!correct)
    {
        printf("ERR\n");
        return 0;
    }


    up(guess);
    up(answer);

    int color[5] = {};//W = 0, Y = 1, G = 2;
    for(int i = 0 ; i < 5 ; i++)
    {
        for(int j = 0 ; j < 5 ; j++)
        {
            if(guess[i] == answer[j])
            {
                color[i] = 1;
            }
        }
        if(guess[i] == answer[i])
        {
                color[i] = 2;
        }
    }

    for(int i = 0 ; i < 5 ; i++)
    {
        switch(color[i])
        {
            case 0:
                printf("W");
                break;
            case 1:
                printf("Y");
                break;
            case 2:
                printf("G");
                break;

        }
    }
    return 0;
}
