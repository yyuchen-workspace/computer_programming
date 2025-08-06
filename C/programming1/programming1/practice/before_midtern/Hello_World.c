#include<stdio.h>
int main()
{
    int times;
    int cases = 1;
    scanf("%d", &times);
    while(10001 > times && times > 0)
    {
        int paste = 0;

        while(times > 1)
        {

            if(times % 2 == 0)
            {
                times /= 2;
                paste++;
            }
            else
            {
                times = (times + 1) / 2;
                paste ++;
            }


        }


        printf("Case %d: %d\n", cases, paste);
        cases++;
        if(cases > 2000)
        {
            return 0;
        }
        scanf("%d", &times);
    }

    return 0;



}
