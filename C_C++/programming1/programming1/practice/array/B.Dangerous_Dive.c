#include<stdio.h>
#include<stdbool.h>
int main()
{

    int come, back;

    while(scanf("%d%d", &come, &back) != EOF)
    {
        int id;
        bool return_num[10001] = {false};

        for(int i = 0 ; i < back ; i++)
        {
            scanf("%d", &id);
            return_num[id] = true;
        }

        bool all_same = true;
        for(int i = 1 ; i <= come ; i++)//½s¸¹¨S¦³0
        {
            if(!return_num[i])
            {
                printf("%d ", i);
                all_same = false;
            }
        }

        if(all_same)
        {
            printf("*");
        }

        printf("\n");



    }
    return 0;
}
