#include <stdio.h>
#include <string.h>
#include <ctype.h>
int ConvertToDigit(const char str[])
{
    char digits[10][10] = {"zero", "one", "two", "three", "four", "five",
                            "six", "seven", "eight", "nine"};
    char tmp[10] = {};
    strcpy(tmp, str);
    for (int i=0, sz=strlen(tmp); i<sz; i+=1)
    {
        tmp[i] = tolower(tmp[i]);
    }

    for (int i=0; i<10; i+=1)
    {
        if (strcmp(tmp, digits[i]) == 0)
        {
            return i;
        }
    }
    return -1;
}


int main()
{
    int t = 0;
    scanf("%d", &t);
    for (int i=0; i<t; i+=1)
    {
        char s[10] = {}, ch = '\0';
        while (scanf("%s%c", s, &ch)==2)
        {
            if (int d = ConvertToDigit(s); d >= 0)
            {
                printf("%d", d);
            }

            if (ch == '\n')
            {
                break;
            }
        }
        puts("");
    }

    return 0;
}
