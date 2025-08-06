#include<stdio.h>
#include<string.h>
#include<ctype.h>



int main()
{
    char A[51] = {};
    char B[51] = {};
    scanf("%50s", A);
    scanf("%50s", B);

    int ctn_A[26] = {};
    for(int i = 0 ; i < strlen(A) ; i++)
    {
        if(isupper(A[i]))
        {
            A[i] = tolower(A[i]);
        }
        ctn_A[A[i] - 'a'] += 1;
    }

    int ctn_B[26] = {};
    for(int i = 0 ; i < strlen(B) ; i++)
    {
        if(isupper(B[i]))
        {
            B[i] = tolower(B[i]);
        }
        ctn_B[B[i] - 'a'] += 1;
    }



    for(int i = 0 ; i < 26 ; i++)
    {
        if(ctn_A[i] != ctn_B[i])
        {
            printf("Not anagrams!\n");
            return 0;
        }
    }

    for(int i = 0 ; i < 26 ; i++)
    {
        if(ctn_A[i] != 0)
        {
            for(int j = 0 ; j < ctn_A[i] ; j++)
            {
                printf("%c", i + 'a');
            }
        }
    }
    printf("\n");
    return 0;
}
