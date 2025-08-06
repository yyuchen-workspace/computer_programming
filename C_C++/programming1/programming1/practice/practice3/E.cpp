#include<stdio.h>
#include<string.h>

int main()
{
    int people, test_case = 0;
    while(scanf("%d", &people) == 1)
    {

        char name[10][13] = {};
        int money[10] = {};
        for(int i = 0 ; i < people ; i++)
        {
            scanf("%s", &name[i]);
        }

        char giver[13] = {};
        int paid, num;
        int got;
        for(int i = 0 ; i < people ; i++)
        {
            scanf("%s %d %d", giver, &paid, &num);
            got = num > 0 ? paid / num : 0;

            for(int j = 0 ; j < people ; j++)
            {
                if(strcmp(name[j], giver) == 0)
                {
                    money[j] -= got*num;
                }
            }

            char taker[13] = {};
            for(int j = 0 ; j < num ; j++)
            {
                scanf("%s", taker);
                for(int k = 0 ; k < people ; k++)
                {
                    if(strcmp(name[k], taker) == 0)
                    {
                        money[k] += got;
                    }
                }
            }


        }
        if(test_case > 0)
        {
            printf("\n");
        }

        for(int i = 0 ; i < people ; i++)
        {
            printf("%s %d\n", name[i], money[i]);
        }
        test_case+=1;

    }
}
