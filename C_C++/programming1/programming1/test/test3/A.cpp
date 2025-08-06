#include<stdio.h>
#include<string.h>
#include<stdbool.h>
int main()
{
    int n;
    while(scanf("%d", &n) == 1 && n <= 3000)
    {
        int arr[3000] = {};
        for(int i = 0 ; i < n ; i++)
        {
            scanf("%d", &arr[i]);
        }

        int minus[2999] = {};
        int num;
        for(int i = 0 ; i < n - 1 ; i++)
        {
            num = arr[i+1] - arr[i];
            if(num < 0)
            {
                num*= -1;
            }
            minus[num] +=1;
        }

        bool is_Jolly= true;
        for(int i = 1 ; i < n ; i++)
        {
            if(minus[i] == 0)
            {
                is_Jolly = false;
            }
        }

        if(is_Jolly)
        {
            printf("Jolly\n");
        }
        else
        {
            printf("Not jolly\n");
        }
    }
}
