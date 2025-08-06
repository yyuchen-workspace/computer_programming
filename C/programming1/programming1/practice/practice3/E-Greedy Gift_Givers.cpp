#include<stdio.h>
#include<string.h>
constexpr int MaxNameLen = 12;

int main()
{
    int quantity = 0, cases = 1;

    while(scanf("%d", &quantity) == 1)
    {
        char name[10][MaxNameLen+1] = {};
        int balance[10] = {};

        for(int i = 0 ; i < quantity ; i++)
        {
            scanf("%s", name[i]);
        }

        for (int i = 0; i < quantity; i++)
        {
            char giver[MaxNameLen+1] = {}, taker[10][MaxNameLen+1] = {};
            int paid = 0, num_takers = 0;
            scanf("%s %d %d", giver, &paid, &num_takers);
            int got = num_takers>0?paid/num_takers:0;
            paid = got*num_takers;

            for (int j=0; j<quantity; j++)
            {
                if (strcmp(name[j], giver) == 0)
                {
                    balance[j] -= paid;
                    break;
                }

            }
            for(int k = 0 ; k < num_takers ; k++)
            {
                    scanf("%s", taker[k]);
                for(int j = 0 ; j < quantity ; j++)
                {
                    if(strcmp(name[j], taker[k]) == 0)
                    {
                        balance[j] += got;
                    }
                }
            }




        }

        if(cases > 1) printf("\n");

        for(int i = 0 ; i < quantity ; i++)
        {
            printf("%s %d\n", name[i], balance[i]);
        }
        cases+=1;



    }


}
