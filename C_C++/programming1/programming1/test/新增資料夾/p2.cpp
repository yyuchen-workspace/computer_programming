#include<stdio.h>

int ConverToDigit(const char str[])
{
    if(str[0] == 'z')//0
    {
        if(str[1] == 'e' && str[2] == 'r'&& str[3] == 'o')
        {
            return 0;
        }

    }
    else if(str[0] == 'o')//1
    {
        if(str[1] == 'n' && str[2] == 'e')
        {
            return 1;
        }

    }
   else if(str[0] == 't')//2,3
    {
        if(str[1] == 'w' && str[2] == 'o')
        {
            return 2;
        }
        else if(str[1] == 'h' && str[2] == 'r' && str[3] == 'e' && str[4] == 'e')
        {
            return 3;
        }
    }
    else if(str[0] == 'f')//4,5
    {
        if(str[1] == 'o' && str[2] == 'u' && str[3] == 'r')
        {
            return 4;
        }
        else if(str[1] == 'i' && str[2] == 'v' && str[3] == 'e' )
        {
            return 5;
        }
    }
    else if(str[0] == 's')//6,7
    {
        if(str[1] == 'i' && str[2] == 'x')
        {
            return 6;
        }
        else if(str[1] == 'e' && str[2] == 'v' && str[3] == 'e'  && str[4] == 'n')
        {
            return 7;
        }
    }
    else if(str[0] == 'e')//8
    {
        if(str[1] == 'i' && str[2] == 'g' && str[3] == 'h'  && str[4] == 't')
        {
            return 8;
        }
    }
    else if(str[0] == 'n')//9
    {
        if(str[1] == 'i' && str[2] == 'n' && str[3] == 'e' )
        {
            return 9;
        }
    }
    else
    {
        return -1;
    }
}





int main()
{
    int t;
    scanf("%d", &t);
    for(int i = 0 ; i < t ; i++)
    {
        char str[6] = {};
        char ch = 0;
        while(scanf("%s%c", str, &ch) == 2)
        {
            int num = ConverToDigit(str);
             printf("%d", num);
        }
        printf("\n")

    }
}
