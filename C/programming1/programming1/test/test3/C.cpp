#include <stdio.h>
#include <string.h>
int main()
{
    constexpr int MaxSize = 100;
    int cases = 1;
    int r = 0, c = 0, t = 1;
    int dx[] = {-1, -1, -1, 0, 0, 1, 1, 1};
    int dy[] = {-1, 0, 1, -1, 1, -1, 0, 1};
    while (scanf("%d%d", &r, &c)==2 && r && c)
    {
        char board[MaxSize+2][MaxSize+2] = {};
        for (int i=1; i<=r; i+=1)
        {
                scanf("%s", &board[i][1]);
        }
        int map[MaxSize+1][MaxSize+1] = {};
        memset(map, 0, sizeof(map));
        for(int i = 1 ; i <= r ; i++)
        {
            for(int j = 1 ; j <= c ; j++)
            {
                if(board[i][j] == '*')
                {
                         map[i][j] = -1;
                }
                else
                {
                    for(int k = 0 ; k < 8 ; k++)
                    {

                        int x = i + dx[k];
                        int y = j + dy[k];
                        if (x >= 1 && x <= r && y >= 1 && y <= c && board[x][y] == '*')
                        {
                            map[i][j] += 1;
                        }
                    }
                }
            }
        }

        if(cases > 1) printf("\n");
        printf("Field #%d:\n", cases);
        for(int i = 1 ; i <= r ; i++)
        {
            for(int j = 1 ; j <= c ; j++)
            {
                if(map[i][j] == -1)
                {
                    printf("*");
                }
                else
                {
                    printf("%d", map[i][j]);
                }
            }
            printf("\n");
        }

        cases+=1;

    }

}

