#include <stdio.h>
#include <string.h>
#include<stdbool.h>
int main()
{
    int T = 0;
    scanf("%d", &T);
    for (int t=1; t<=T; t+=1)
    {
        char dummy;
        int n = 0;
        bool Symmetric = true;
        scanf(" %c %c %d", &dummy, &dummy, &n);
        long long int matrix[100][100] = {};
        for (int i=0; i<n; i+=1)
        {
            for (int j=0; j<n; j+=1)
            {
                scanf("%lld", &matrix[i][j]);
                if(matrix[i][j] < 0) Symmetric = false;
            }

        }
        if(!Symmetric)
        {
            printf("Test #%d: Non-symmetric.\n", t);
            continue;
        }

        for (int i=0 ; i <= n / 2 ; i+=1)
        {
            for (int j=0; j< n; j+=1)
            {
                if(matrix[i][j] != matrix[n - 1 - i][n - 1 - j])
                {
                    Symmetric = false;
                    break;
                }
            }
        }

        if(Symmetric) printf("Test #%d: Symmetric.\n", t);
        else printf("Test #%d: Non-symmetric.\n", t);

    }
}
