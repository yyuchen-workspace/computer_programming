#include<stdio.h>
#include<string.h>
#include<ctype.h>

int main()
{
    char word[200];
    char output[200][200];
    int times = 0;
    while (scanf("%s", word) != EOF)
    {
        int sz = strlen(word);
        int temp_sz = sz;
        for(int i = 0  ; i < temp_sz  ; i++)
        {
            output[times][i] = word[sz - 1];
            sz--;
        }
        printf("%s", output[times]);
        times++;
        printf(" ");
    }
}

