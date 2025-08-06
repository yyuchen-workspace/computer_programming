#include<stdio.h>

int main()
{
    int lines;

    for(int i = 1 ; i <= 2000 ; i++)
    {
        int paste = 0;
        scanf("%d", &lines);
        if(lines < 0)
        {
            break;
        }

        while(lines / 2 > 0)
        {
            if(lines % 2 != 0)
            {
                lines += 1;
            }

            lines /= 2;
            paste++;
        }

        printf("Case %d: %d\n", i, paste);
    }
    return 0;
}
