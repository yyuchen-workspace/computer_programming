#include<stdio.h>
#include<string.h>
constexpr int MAXSIZE = 100;

int main()
{
    int row, column, test_case = 1;
    int dx[] = {-1, 0, 1, -1, 1, -1, 0 ,1};
    int dy[] = {-1, -1, -1, 0, 0, 1, 1, 1};
    while(scanf("%d %d", &row, &column) == 2 &&row && column)
    {
        char mine[MAXSIZE+2][MAXSIZE+2] = {};
        for(int i = 1 ; i <= row ; i++)
        {
            scanf("%s", &mine[i][1]);
        }

        int map[MAXSIZE+1][MAXSIZE+1] = {};
        for(int i = 1 ; i <= row ; i++)
        {
            for(int j = 1 ; j <= column ; j++)
            {
                if(mine[i][j] == '*')
                {
                    map[i][j] = -1;
                }
                else
                {
                    for(int k = 0 ; k < 8 ; k++)
                    {
                        int x = i + dy[k];
                        int y = j + dx[k];
                        if (x >= 1 && x <= row && y >= 1 && y <= column && mine[x][y] == '*')
                        {
                            map[i][j] += 1;
                        }
                    }
                }
            }
        }

        if(test_case > 1) printf("\n");
        printf("Field #%d:\n", test_case);

        for(int i = 1 ; i <= row ; i++)
        {
            for(int j = 1 ; j <= column ; j++)
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

        test_case+=1;

    }
}
