#include<stdio.h>
#include<string.h>


int main()
{
    int m;
    scanf("%d", &m);
    for(int t = 0 ; t < m ; t++)
    {
        char En[4] = {};
        char dash;
        scanf("%3s %c", En, &dash);


        int num;

        scanf("%d", &num);


        int pluss = 0;
        int cln = 0;
        int p = 676;
        for(int i = 0 ; i < 3 ; i++)
        {
            cln = En[i] - 'A';
            pluss += cln * p;
            p /=26;
        }



        int cal = pluss - num;
        if(cal < 0)
        {
            cal*=-1;
        }

        if(cal<=100)
        {
            printf("nice\n");
        }
        else
        {
            printf("not nice\n");
        }


    }
}
