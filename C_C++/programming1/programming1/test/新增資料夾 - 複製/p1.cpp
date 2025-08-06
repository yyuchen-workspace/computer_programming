#include<stdio.h>
#include<string.h>
int main()
{
    int t;
    scanf("%d", &t);
    char map[11][11] = {};
    for(int i = 0 ; i < t ; i++)
    {
        scanf("%s", map[i]);
    }

    int boom = 0;
    for(int i = 0 ; i < t ; i++)
    {
        for(int j = 0 ; j < t ; j++)
        {
            if(map[i][j] != 'X' && map[i][j] != '.' && map[i][j] != 'O')
            {
                boom = map[i][j] - '0';
                for(int k = 1 ; k <= boom ; k++)
                {
                    if(map[i+k][j] == 'X' || i+k > 10)
                    {
                        break;
                    }
                    map[i+k][j] = 'O';

                }
                for(int k = 1 ; k <= boom ; k++)
                {
                    if(map[i-k][j] == 'X' || i-k < 0)
                    {
                        break;
                    }
                    map[i-k][j] = 'O';

                }
                for(int k = 1 ; k <= boom ; k++)
                {
                    if(map[i][j+k] == 'X' || j+k > 10)
                    {
                        break;
                    }
                    map[i][j+k] = 'O';

                }
                for(int k = 1 ; k <= boom ; k++)
                {
                    if(map[i][j-k] == 'X' || j-k < 0)
                    {
                        break;
                    }
                    map[i][j-k] = 'O';

                }


            }
        }
    }

    for(int i = 0 ; i < t ; i++)
    {
        for(int j = 0 ; j < t ; j++)
        {
            printf("%c", map[i][j]);
        }
        printf("\n");

    }
}

