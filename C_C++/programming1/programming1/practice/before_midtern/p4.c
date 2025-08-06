#include<stdio.h>
#include<stdbool.h>
int main()
{
    int shop, Number_of_people, candidate[10] = {0}, vote[10] = {0};
    scanf("%d%d", &shop, &Number_of_people);
    for(int i = 0 ; i < shop ; i++)
    {

        for(int j = 0 ; j < Number_of_people ; j++)
        {
            scanf("%d", &candidate[j]);
        }


        for(int j = 0 ; j < Number_of_people ; j++)
        {
            bool win = true;
            for(int k = 0 ; k < Number_of_people ; k++)
            {
                if(candidate[j] < candidate[k])
                {
                    win = false;
                    break;
                }
            }
            if(win == true)
            {
                vote[j]++;
            }
        }

    }

    for(int i = 0 ; i < Number_of_people ; i++)
        {
            bool win = true;
            for(int j = 0 ; j < Number_of_people ; j++)
            {
                if(vote[i] < vote[j])
                {
                    win = false;
                    break;
                }
            }
            if(win == true)
            {
                int temp = i + 1;
                printf("%d ", temp);
            }
        }
    return 0;

}
