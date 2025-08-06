#include<stdio.h>
#include<string.h>
#include<stdbool.h>

int main()
{
    int T;
    scanf("%d", &T);
    for(int t = 1 ; t <= T ; t++)
    {

        char dummy;
        int row;
        bool Symmetric = true;
        long long int n[100][100] = {};
        scanf(" %c %c %d", &dummy,&dummy, &row);
        for(int i = 0 ; i < row ; i++)
        {
            for(int j = 0 ; j < row ; j++)
            {
                scanf("%lld", &n[i][j]);
                if(n[i][j] < 0)
                {
                    Symmetric = false;
                }
            }
        }

        printf("Test #%d: ", t);

        if(!Symmetric)
        {
            printf("Non-symmetric.\n");
            continue;
        }


        for(int i = 0 ; i < row ; i++)
        {
            for(int j = 0 ; j < row ; j++)
            {
                if(n[i][j] != n[row - i - 1][row - j - 1])
                {
                    Symmetric = false;
                    break;
                }
            }
        }

        if(Symmetric)
        {
            printf("Symmetric.\n");
        }
        else
        {
            printf("Non-symmetric.\n");
        }

    }

    return 0;
}
