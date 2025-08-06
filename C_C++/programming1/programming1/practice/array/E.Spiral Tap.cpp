#include <stdio.h>
#include<stdint.h>
int main()
{
    int32_t SZ, P;
    int32_t spiral[50][50] = {0};
    scanf("%d%d", &SZ, &P);
    while(SZ < 0 || SZ % 2 == 0)
    {
        scanf("%d%d", &SZ, &P);
    }

    while(SZ != 0 && P != 0)
    {

        int32_t mid = SZ / 2;
        int32_t row = 0, column = 0;
        int32_t temp = 1;//開始點
        spiral[mid][mid] = temp;

        for(int i = 0; i < SZ; i += 2)
        {
            row = mid - i / 2;//找起點
            column = mid + i / 2;//找起點

            //row不變
            for(int first = 0; first < i; first++)
            {
                column -= 1;
                temp += 1;
                spiral[row][column] = temp;


            }

            //column不變
            for(int second = 0; second < i; second++)
            {
                row += 1;
                temp += 1;
                spiral[row][column] = temp;

            }

            //row不變
            for(int third = 0 ; third < i; third++)
            {
                column += 1;
                temp += 1;
                spiral[row][column] = temp;

            }

            //column不變
            for(int forth = 0; forth < i; forth++)
            {
                row -= 1;
                temp += 1;
                spiral[row][column] = temp;

            }

        }
        for(int i = 0 ; i < SZ ; i++)
        {
            for(int j = 0 ; j < SZ ; j++)
            {
                printf("%d ", spiral[i][j]);
/*
                if(spiral[i][j] == P)
                {
                    j += 1;
                    i = (i - SZ) * -1 ;


                    printf("Line = %d, column = %d.\n", i, j);
                }
                */

            }

            printf("\n");
        }

        scanf("%d%d", &SZ, &P);
        while(SZ != 0 && (SZ < 0 || SZ % 2 == 0))
        {
            scanf("%d%d", &SZ, &P);
        }
    }

}

