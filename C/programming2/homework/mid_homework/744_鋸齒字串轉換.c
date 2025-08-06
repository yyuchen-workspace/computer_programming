#include<stdio.h>
#include<string.h>
#include<stdbool.h>


int main()
{
    int n;
    char s[1001];
    scanf("%d", &n);
    scanf("%s", s);

    if (n == 1) {
        printf("%s\n", s);
        return 0;
    }

    int len = strlen(s);
    char rows[50][1001] = {};
    int pos[50] = {0};

    int row = 0;
    bool down = true;
    for(int i = 0 ; i < len ; ++i)
    {
        rows[row][pos[row]++] = s[i];

        if(down)
        {
            if(row == n - 1)
            {
                row--;
                down = false;
            }
            else
            {
                row++;
            }
        }
        else
        {
            if(row == 0)
            {
                row++;
                down = true;
            }
            else
            {
                row--;
            }
        }
    }

    for(int i = 0 ; i < n ; ++i)
    {
        rows[i][pos[i]] = '\0';
        printf("%s", rows[i]);
    }

    printf("\n");

}
