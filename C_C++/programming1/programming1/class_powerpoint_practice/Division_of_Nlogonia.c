#include<stdio.h>
int main()
{
    int times;
    scanf("%d", &times);
    while(times != 0)
    {
        int N = 0, M = 0;
        scanf("%d %d", &N, &M);
        for(int i = 0 ; i < times ; i++)
        {
            int X, Y;
            scanf("%d %d", &X, &Y);
            if(X == N || Y == M)
            {
                printf("divisa\n");
            }
            else if(X < N && Y > M)
            {
                printf("NO\n");
            }
            else if(X > N && Y > M)
            {
                printf("NE\n");
            }
            else if(X > N && Y < M)
            {
                printf("SE\n");
            }
            else
            {
                printf("SO\n");
            }
        }

        scanf("%d", &times);
    }

    return 0;
}
