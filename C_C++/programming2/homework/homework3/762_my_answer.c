#include<stdio.h>
#include<string.h>
#define max 101
int main()
{
    char s[max], t[max];
    scanf("%s", s);
    scanf("%s", t);

    char temp_s[max];
    char temp_t[max];
    int top_s = 0;
    for(int i = 0 ; i < strlen(s) ; i++)
    {
        if(s[i] != '#')
        {
            temp_s[top_s++] = s[i];
        }
        else
        {
            if (top_s > 0) top_s--;
        }
    }
    temp_s[top_s] = '\0';

    int top_t = 0;
    for(int i = 0 ; i < strlen(t) ; i++)
    {
        if(t[i] != '#')
        {
            temp_t[top_t++] = t[i];
        }
        else
        {
            if (top_t > 0) top_t--;
        }

    }
    temp_t[top_t] = '\0';


    if(strcmp(temp_s, temp_t) == 0)
    {
        printf("true");
    }
    else
    {
        printf("false");
    }



}


