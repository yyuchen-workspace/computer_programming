#include<stdio.h>

int main()
{
    int SZ, P;
    scanf("%d%d", &SZ, &P);
    while(SZ != 0 || P != 0)
    {
        int mid = SZ / 2;
        if(P == 1)
        {
            printf("Line = %d, column = %d.\n", mid+1, mid+1);
            scanf("%d%d", &SZ, &P);
            continue;
        }

        int circle, start_row, start_column, last_circle;
        for(int i = 1 ; i <= SZ ; i+=2)
        {
            if(P <= i * i)
            {
                circle = i / 2 + 1;
                if(circle == 2)
                {
                    start_row = mid - 1;
                    start_column = mid;

                }
                else
                {
                    start_row = mid - 1 - (circle - 2);
                    start_column = mid + (circle - 2);

                }
                last_circle = (i-1)*(i-1);
                break;
            }
        }
        int move = (circle - 1) * 2;
        int left = -(move-1), down = move, right = move, up = -move;
        int steps = P - last_circle;
        int go;
        if((steps-1) / move < 1)
        {
            go = steps - 1;
            start_column -= go;
        }
        else if((steps-1) / move < 2)
        {
            go = steps - move;
            start_column += left;
            start_row += go;
        }
        else if((steps-1) / move < 3)
        {
            go = steps - move*2;
            start_column += left + go;
            start_row += down;
        }
        else if((steps-1) / move < 4)
        {
            go = steps - move*3;
            start_column += left + right;
            start_row += down - go;
        }
        start_row = SZ - start_row;
        start_column +=1;
        printf("Line = %d, column = %d.\n", start_row, start_column);

        scanf("%d%d", &SZ, &P);
    }
}
