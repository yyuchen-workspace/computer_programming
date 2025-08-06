#include<stdio.h>
#include<string.h>
#define max 101

int main()
{
    char cnt[26] = {};
    char str[max] = {};
    char output[max] = {};
    int count = 0;

    scanf("%s", cnt);
    scanf("%s", str);
    for(int i = 0 ; i < 26 ; i++)
    {
        for(int j = 0 ; j < strlen(str) ; j++)
        {
            if(str[j] == cnt[i])
            {
                output[count++] = str[j];
            }
        }
    }

    printf("%s\n", output);

}
