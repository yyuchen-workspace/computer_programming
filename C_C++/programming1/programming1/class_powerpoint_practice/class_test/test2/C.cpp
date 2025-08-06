#include<stdio.h>
#include<stdint.h>
int main()
{
    int32_t W, H, N;
    scanf("%d%d%d", &W, &H, &N);
    while(W == 0 && H == 0 && N == 0)
    {
        int32_t board[99][4];
        for(int i = 0 ; i < N ; i++)
        {
            for(int j = 0 ; j < 4 ; j++)
            {
                scanf("%d", &board[i][j]);
            }
        }


        scanf("%d%d%d", &W, &H, &N);
    }
}
