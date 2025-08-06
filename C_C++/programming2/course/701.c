#include<stdio.h>
#include<string.h>
#include<stdbool.h>

int main()
{
    char password[51] = {};
    scanf("%s", password);

    if(strlen(password) < 8)
    {
        printf("false");
        return 0;
    }

    bool lower = false;
    bool upper = false;
    bool digit = false;
    bool symbol = false;

    for(int i = 0 ; i < strlen(password) ; i++)
    {
        if(islower(password[i]))
        {
            lower = true;
        }
        else if(isupper(password[i]))
        {
            upper = true;
        }
        else if(isdigit(password[i]))
        {
            digit = true;
        }
        else
        {
            symbol = true;
        }
    }

    if(lower && upper && digit && symbol)
    {
        printf("true\n");
    }
    else
    {
        printf("false\n");
    }

    return 0;
}
