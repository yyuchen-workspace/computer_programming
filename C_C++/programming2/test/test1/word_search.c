#include<stdio.h>
#include<string.h>
#include<ctype.h>


int main()
{
    char S[101] = {};
    char K[101] = {};
    int ans = 0;
    scanf("%s", S);
    scanf("%s", K);
    int length = strlen(K);
    for(int i = 0 ; i < strlen(S) ; i++)
    {


        if(strncmp(S+i, K, length) == 0)
        {
            break;
        }
        ans++;
    }
    if(ans == strlen(S))
    {
        printf("-1");
    }
    else
    {
        printf("%d\n", ans);
    }
}

