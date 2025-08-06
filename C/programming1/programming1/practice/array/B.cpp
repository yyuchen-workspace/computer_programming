#include<stdio.h>
#include<stdbool.h>
int main()
{
    int go, back_num;
    while(scanf("%d%d", &go, &back_num) == 2)
    {
        bool is_back[10000] = {false};
        bool all_back = true;
        int back;

        for(int i = 0 ; i < back_num ; i++)
        {
            scanf("%d", &back);
            is_back[back] = true;
        }

        for(int i = 1 ; i <= go ; i++)
        {
            if(!is_back[i])
            {
                printf("%d ", i);
                all_back = false;
            }
        }


        if(all_back)
        {
            printf("*");
        }
        printf("\n");
    }


}
